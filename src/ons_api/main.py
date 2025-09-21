from fastapi import FastAPI, Query, HTTPException, BackgroundTasks
from ons_api.models import PostFiltro
from ons_api.service import ONSService
from typing import Optional
from datetime import datetime
from ons_api.logging_config import setup_logging

logger = setup_logging()

app = FastAPI(title= "ONS EAR API")
service = ONSService()


@app.get("/dados")
def get_dados(
    start_date: str = Query(..., description="Data de início dos dados"),
    end_date: Optional[str] = Query(None, description="Data final dos dados"),
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(50, ge=1, le=500, description="Tamanho da página"),
):
    logger.info(f"GET /dados called with start_date={start_date}, end_date={end_date}, page={page}, page_size={page_size}")
    try:
        df = service.search_data(start_date, end_date)
        return service.pagination(df, page, page_size)
    except Exception as e:
        logger.error(f"Error on GET/dados: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/export-to-gcs")
def export_all_data(background_tasks: BackgroundTasks):   
    logger.info("POST /export-to-gcs started")
    try:
        df = service.search_data(start_date="01-01-2000", end_date=datetime.today().strftime("%d-%m-%Y"))

        if df.empty:
            logger.warning("None data found to export.")
            raise HTTPException(status_code=404, detail="None data found to export.")

        # dispara o processamento em segundo plano
        background_tasks.add_task(process_export, df)

        return {"message": "Export job started, check status later."}

    except Exception as e:
        logger.error(f"Error on export-to-gcs: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


def process_export(df):
    blob_path = service.upload_parquet_to_bucket(df)
    table_ref = service.load_to_bigquery(df)
    logger.info(f"✅ Export done! File: {blob_path}, Table: {table_ref}")