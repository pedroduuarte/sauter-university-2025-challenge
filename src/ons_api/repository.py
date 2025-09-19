from fastapi import FastAPI, Query, HTTPException
import pandas as pd
import requests
import os
import json
from io import BytesIO
from datetime import datetime

app = FastAPI(title="Teste de API para dados dos reservatórios ONS")


class ONSRepository:
    URL_PACKAGE_SEARCH = "https://dados.ons.org.br/api/3/action/package_search?q=ear-diario-por-reservatorio"
    RESOURCES_CACHE = "resources.json"

    def search_all_resources(self):
        """
        Busca todos os resources disponíveis no dataset.
        """
        # checa se o cache existe para otimização de performance
        if os.path.exists(self.RESOURCES_CACHE):
            with open(self.RESOURCES_CACHE, "r", encoding="utf-8") as f:
                return json.load(f)
        
        # caso não exista, busca da ONS
        resp = requests.get(ONSRepository.URL_PACKAGE_SEARCH)
        if resp.status_code != 200:
            raise HTTPException(status_code=500, detail="Erro ao consultar o package_search.")
        
        data = resp.json()
        package = data["result"]["results"][0]  # primeiro dataset
        resources = package["resources"]

        # filtrando arquivos csv
        csv_resources = [
            {
                "id": r["id"],
                "name": r["name"],
                "url": r["url"]
            }
            for r in resources if r["format"].lower() == "csv"
        ]

        with open(self.RESOURCES_CACHE, "w", encoding="utf-8") as f:
            json.dump(resources, f, ensure_ascii=False, indent=2)

        return csv_resources
    
    def download_csv(self, url: str) -> pd.DataFrame:
        resp = requests.get(url)
        if resp.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Failed to download data from {url}")
        df = pd.read_csv(BytesIO(resp.content), sep=';', encoding='utf-8') 
        return df
    
    def date_validation(self, start_date: str, end_date: str): 
        """
        Valida as datas para os intervalos
        """
        try:
            start = datetime.strptime(start_date, "%d-%m-%Y")
            if end_date:
                end = datetime.strptime(end_date, "%d-%m-%Y")
            else: 
                end = datetime.today()
        except ValueError:
            raise HTTPException(status_code=400, detail="Dates must be formatted dd-mm-yyyy")
        
        if start > end:
            raise HTTPException(status_code=400, detail="Start date must be bigger than end date.")
        
        return start, end

            
    def exctrat_files_from_interval(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Carrega os dados de acordo com o intervalo de datas passadas como parâmetro
        """
        start, end = self.date_validation(start_date, end_date)
        years = range(start.year, end.year + 1)
        resources = self.search_all_resources()

        dfs = []
        for year in years:
            resource = next((r for r in resources if str(year) in r["name"]), None)
            if not resource:
                print(f"Not found any resource for {year}")
                continue

            df = self.download_csv(resource["url"])
            print("DEBUG DF:", type(df))
            if df is None:
             print("DataFrame é None!")
            else:
                print("Colunas disponíveis:", df.columns)
            df["Data"] = pd.to_datetime(df["ear_data"], errors="coerce")
            df = df[(df["Data"] >= start) & (df["Data"] < end)]
            dfs.append(df)

        if not dfs:
            raise HTTPException(status_code=404, detail="Not found any data in the interval.")
        
        return pd.concat(dfs, ignore_index=True)
            
