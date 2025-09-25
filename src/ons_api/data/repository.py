from fastapi import HTTPException
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO
from datetime import datetime
from ..core.logging_config import setup_logging

logger = setup_logging()

class ONSRepository:
    PACKAGE_ID = "61e92787-9847-4731-8b73-e878eb5bc158"
    URL_PACKAGE_SHOW = "https://dados.ons.org.br/api/3/action/package_show?id="
    URL_RESOURCE_SHOW = "https://dados.ons.org.br/api/3/action/resource_show?id="


    def search_all_resources(self):
        """
        Search all resources avaliable on dataset.
        """
        resp = requests.get(f"{self.URL_PACKAGE_SHOW}{self.PACKAGE_ID}")
        if resp.status_code != 200:
            logger.error(f"Error on trying to get all resources from EAR")
            raise HTTPException(status_code=500, detail="Erro ao consultar o package_search.")
        
        data = resp.json()
        package = data["result"]
        resources = package["resources"]

        # filter csv files
        csv_resources = [
            {
                "id": r["id"],
                "name": r["name"],
                "url": r["url"]
            }
            for r in resources if r["format"].lower() == "csv"
        ]

        return csv_resources
    
    def get_resource_url(self, resource_id: str):
        resp = requests.get(f"{self.URL_RESOURCE_SHOW}{resource_id}")
        if resp.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Failed to fetch resource id from: {resource_id}")
        data = resp.json()
        return data["result"]["url"]
    
    def download_csv_by_id(self, resource_id: str) -> pd.DataFrame:
        """
        Download the resource by the resource id
        """
        url = self.get_resource_url(resource_id)
        resp = requests.get(url)
        if resp.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Failed to download data from {url}")
        df = pd.read_csv(BytesIO(resp.content), sep=';', encoding='utf-8') 
        return df
    
    def date_validation(self, start_date: str, end_date: str): 
        """
        Validate dates for the intervals
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
        Load files by the date interval
        """
        start, end = self.date_validation(start_date, end_date)
        years = range(start.year, end.year + 1)
        resources = self.search_all_resources()

        dfs_by_year = {}

        def process_year(year):
            resource = next((r for r in resources if str(year) in r["name"]), None)
            if not resource:
                logger.warning(f"No resource found for {year}")
                return None, None
            df = self.download_csv_by_id(resource["id"])

            df = df[(df["ear_data"] >= start_date) & (df["ear_data"] <= end_date)]
            return year, df
        
        with ThreadPoolExecutor(max_workers=3) as pool: 
            futures = {pool.submit(process_year, year): year for year in years}
            for future in as_completed(futures):
                year, df = future.result()
                if year and df is not None:
                    dfs_by_year[year] = df
        if not dfs_by_year:
            raise HTTPException(status_code=404, detail="Not found any data in the interval.")
        
        return dfs_by_year

            
