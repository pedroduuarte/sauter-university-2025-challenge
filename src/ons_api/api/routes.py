from fastapi import Query, HTTPException, APIRouter
from ..api.schemas import PostFilter
from ..data.GCPHandler import GCPHandler
from ..services.ons_service import ONSService
from typing import Optional
from ..core.logging_config import setup_logging
from datetime import datetime

logger = setup_logging()
router = APIRouter()
service = ONSService()
handler = GCPHandler()


@router.get("/data", tags=["ONS Data"])
def get_data(
    start_date: str = Query(..., description="Start date (dd-mm-yyyy)", example="01-01-2024"),
    end_date: Optional[str] = Query(None, description="End date (dd-mm-yyyy)", example="31-04-2024"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=500, description="Page size"),
):
    logger.info(f"GET /dados called with start_date={start_date}, end_date={end_date}, page={page}, page_size={page_size}")
    try:
        start_date_fmt = datetime.strptime(start_date, "%d-%m-%Y").strftime("%Y-%m-%d")
        end_date_fmt = None
        if end_date:
            end_date_fmt = datetime.strptime(end_date, "%d-%m-%Y").strftime("%Y-%m-%d")

        return service.search_data_bq(start_date_fmt, end_date_fmt, page, page_size)
    except Exception as e:
        logger.error(f"Error on GET/dados: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/data", tags=["ONS Data"])
def export_all_data(payload: PostFilter):   
    logger.info("POST /export-to-gcs started")

    try:
        dfs_by_year = service.search_data(
            start_date=payload.start_date,
            end_date=payload.end_date
        )

        if not dfs_by_year:  
            logger.warning("No data found to export.")
            raise HTTPException(status_code=404, detail="No data found to export.")

       
        uploaded_files, did_upload = handler.upload_parquet_to_bucket(dfs_by_year)
        if did_upload:
            return {
            "message": "Data exported successfully",
            "files_uploaded": uploaded_files
            }
        else: 
            return {
                "message": "No new data to export today",
                "files_already_exists": uploaded_files
            }
            
    except Exception as e:
        logger.error(f"Error on export-to-gcs: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
