from fastapi import FastAPI, Query
from ons_api.models import PostFiltro
from ons_api.service import ONSService
from typing import Optional

app = FastAPI(title= "ONS EAR API")
service = ONSService()

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
    df = service.search_data(filter.ano, filter.start_date, filter.end_date)
    return service.paginar(df, filter.page, filter.page_size)