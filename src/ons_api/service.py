import pandas as pd
from datetime import datetime
from google.cloud import storage, bigquery
from ons_api.repository import ONSRepository
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()

class ONSService:
    def __init__(self):
        self.repo = ONSRepository()
        self.project_id = os.getenv("PROJECT_ID")
        self.bucket_name = os.getenv("BUCKET_NAME")
        self.bq_dataset = os.getenv("BQ_DATASET")
        self.table_ref = os.getenv("BQ_TABLE")

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
    
    def upload_parquet_to_bucket(self, df: pd.DataFrame, source_name="ONS", file_type="PARQUET"):
        """
        Uploading dataframe in a GCP bucket using Cloud Run
        """
        client = storage.Client(project=self.project_id)
        bucket = client.bucket(self.bucket_name)

        # upload date 
        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")

        file_name = f"ons_data_{now.strftime('%Y%m%d')}.parquet"
        blob_path = f"raw/{source_name}/{file_type}/{year}/{month}/{day}/{file_name}"

        blob = bucket.blob(blob_path)

        buffer = BytesIO()
        df.to_parquet(buffer, engine="pyarrow", index=False)
        buffer.seek(0)

        blob.upload_from_file(buffer, content_type="application/octet-stream")
        print(f"File uploaded to gs://{bucket}/{blob_path}")

        return blob_path
    
    def load_to_bigquery(self, df: pd.DataFrame):
        """
        load DataFrame to BigQuery (all columns as STRING)
        """
        client = bigquery.Client(project=self.project_id)

        df = df.astype(str)

        table = f"{self.project_id}.{self.bq_dataset}.{self.table_ref}"
        job_config = bigquery.LoadJobConfig(
            write_disposition = bigquery.WriteDisposition.WRITE_APPEND
        )

        job = client.load_table_from_dataframe(df, table, job_config=job_config)
        job.result()

        print(f"Data loaded on BigQuery: {table}")
        return table


