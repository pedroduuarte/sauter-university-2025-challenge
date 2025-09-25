from ..data.repository import ONSRepository
from ..data.GCPHandler import GCPHandler
import pandas as pd

class ONSService:
    def __init__(self):
        self.repo = ONSRepository()
        self.gcp_handler = GCPHandler()

    def search_data(self, start_date=None, end_date=None):
         """ Orchestrate the data search from repository """ 
         return self.repo.exctrat_files_from_interval(start_date, end_date) 

    def search_data_bq(self, start_date: str, end_date: str, page: int, page_size: int):
        """
        Orchestrate search from BigQuery with safe handling of nulls for all column types.
        """
        # search on BigQuery
        df, total = self.gcp_handler.query_bigquery(start_date, end_date, page, page_size)

        # deal with columns by column type
        for col in df.columns:
            if pd.api.types.is_integer_dtype(df[col]) or pd.api.types.is_float_dtype(df[col]):
                # fill null with 0
                df[col] = df[col].fillna(0)
            elif pd.api.types.is_datetime64_any_dtype(df[col]) or str(df[col].dtype).startswith("dbdate"):
                # convert dates to string and fill null with ""
                df[col] = df[col].astype(str).fillna("")
            else:
                # strings and other types: fill null with ""
                df[col] = df[col].fillna("").astype(str)

        return {
            "total": int(total),
            "page": page,
            "page_size": page_size,
            "data": df.to_dict(orient="records")
        }
