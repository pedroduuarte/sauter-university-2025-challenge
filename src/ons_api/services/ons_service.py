from ..data.repository import ONSRepository
from ..data.GCPHandler import GCPHandler

class ONSService:
    def __init__(self):
        self.repo = ONSRepository()
        self.gcp_handler = GCPHandler()

    def search_data_bq(self, start_date: str, end_date: str, page: int, page_size: int):
        """
        Orchestrate search from BQ
        """
        # search on BigQuery
        df, total = self.gcp_handler.query_bigquery(start_date, end_date, page, page_size)

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "data": df.fillna(0).to_dict(orient="records")
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