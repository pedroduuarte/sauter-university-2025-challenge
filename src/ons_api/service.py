import pandas as pd
from ons_api.repository import ONSRepository

class ONSService:
    def __init__(self):
        self.repo = ONSRepository()

    def search_data(self, start_date=None, end_date=None):
        """
        Orquestra a busca de dados do repositório
        """
        return self.repo.exctrat_files_from_interval(start_date, end_date)

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
    
