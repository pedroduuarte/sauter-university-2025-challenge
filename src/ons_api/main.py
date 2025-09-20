from fastapi import FastAPI, Query, HTTPException
from ons_api.models import PostFiltro
from ons_api.service import ONSService
from typing import Optional
from datetime import datetime

app = FastAPI(title= "ONS EAR API")
service = ONSService()
BUCKET_NAME = "sauter-bucket-2025"

@app.get("/dados")
def get_dados(
    start_date: str = Query(..., description="Data de início dos dados"),
    end_date: Optional[str] = Query(None, description="Data final dos dados"),
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(50, ge=1, le=500, description="Tamanho da página"),
):
    df = service.search_data(start_date, end_date)
    return service.pagination(df, page, page_size)

@app.post("/dados")
def post_dados(filter: PostFiltro):
    df = service.search_data(filter.start_date, filter.end_date)
    return service.paginar(df, filter.page, filter.page_size)

@app.post("/export-to-gcs")
def export_all_data():   
    try:
        df = service.search_data(start_date="01-01-2000", end_date=datetime.today().strftime("%d-%m-%Y"))
        
        if df.empty:
            raise HTTPException(status_code=404, detail="Nenhum dado encontrado para exportar.")

        blob_path = service.upload_parquet_to_bucket(df, BUCKET_NAME)
        return {"message": "Dados exportados com sucesso!", "file": blob_path}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))