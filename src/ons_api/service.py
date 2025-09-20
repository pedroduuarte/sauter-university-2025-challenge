import pandas as pd
import datetime
from google.cloud import storage
from ons_api.repository import ONSRepository
from io import BytesIO

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
    
    def upload_parquet_to_bucket(df: pd.DataFrame, bucket_name: str, source_name="ONS", file_type="PARQUET"):
        """
        Uploading dataframe in a GCP bucket using Cloud Run
        """
        client = storage.Client()
        bucket = client.bucket(bucket_name)

        # upload date 
        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")

        file_name = f"ons_data_{now.strftime("%Y%m%d")}.parquet"
        blob_path = f"raw/{source_name}/{file_type}/{year}/{month}/{day}/{file_name}"

        blob = bucket.blob(blob_path)

        buffer = BytesIO()
        df.to_parquet(buffer, engine="pyarrow", index=False)
        buffer.seek(0)

        blob.upload_from_file(buffer, content_type="application/octet-stream")
        print(f"File uploaded to gs://{bucket_name}/{blob_path}")

        return blob_path
    
