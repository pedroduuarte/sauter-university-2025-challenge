from ..data.repository import ONSRepository
from ..data.GCPHandler import GCPHandler

class ONSService:
    def __init__(self):
        self.repo = ONSRepository()
        self.gcp_handler = GCPHandler()

    def search_data(self, start_date=None, end_date=None):
         """ Orquestra a busca de dados do repositório """ 
         return self.repo.exctrat_files_from_interval(start_date, end_date) 

    def search_data_bq(self, start_date: str, end_date: str, page: int, page_size: int):
        """
        Orchestrate search from BQ
        """
        # search on BigQuery
        df, total = self.gcp_handler.query_bigquery(start_date, end_date, page, page_size)

        for col in df.select_dtypes(include=["datetime64[ns]", "dbdate"]).columns:
            df[col] = df[col].astype("string").fillna("")

        for col in df.select_dtypes(exclude=["datetime64[ns]", "dbdate"]).columns:
            df[col] = df[col].fillna("").astype(str)

        return {
            "total": int(total),
            "page": page,
            "page_size": page_size,
            "data": df.fillna("").astype(str).to_dict(orient="records")
        }

    '''
    def pagination(self, df: pd.DataFrame, page: int, page_size: int):
        total = len(df)
        start = (page - 1) * page_size
        end = start + page_size

        data = df.iloc[start:end].fillna(0).to_dict(orient="records")
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "data": data
        }
    '''