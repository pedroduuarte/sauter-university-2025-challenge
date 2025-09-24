import pandas as pd
from datetime import datetime
from google.cloud import storage, bigquery
from io import BytesIO
import os
from dotenv import load_dotenv
from ..core.logging_config import setup_logging

logger = setup_logging()
load_dotenv()

class GCPHandler:
    def __init__(self):
        self.project_id = os.getenv("PROJECT_ID")
        self.bucket_name = os.getenv("BUCKET_NAME")
        self.bq_dataset = os.getenv("BQ_DATASET")
        self.table_ref = os.getenv("BQ_TABLE")
        self.storage_client = storage.Client(project=self.project_id)
        self.bucket = self.storage_client.bucket(self.bucket_name)

    def _normalize_date(self, date_str: str) -> str:
        """
        Converte data para formato YYYY-MM-DD aceito pelo BigQuery.
        Aceita entradas nos formatos DD-MM-YYYY e YYYY-MM-DD.
        """
        for fmt in ("%d-%m-%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
        raise ValueError(f"Formato de data inválido: {date_str}. Use DD-MM-YYYY ou YYYY-MM-DD.")
        
    def blob_exists(self, blob_name: str) -> bool:
        """
        Check if a blob exists in GCS bucket.
        """
        return self.bucket.blob(blob_name).exists()
    
    def check_today_ingestion(self, source_name="ons") -> list:
        """
        Check if there are already files ingested today.
        Returns a list of blob names if they exist.
        """
        now = datetime.now()
        day = now.strftime("%d")
        month = now.strftime("%m")
        year = now.strftime("%Y")

        today_prefix = f"raw/{source_name}/dt={day}-{month}-{year}/"
        blobs_today = list(self.bucket.list_blobs(prefix=today_prefix))

        if blobs_today:
            logger.info(f"Ingestion for {day}-{month}-{year} was already made it.")
            return [blob.name for blob in blobs_today]

        return []
    
    def upload_parquet_to_bucket(self, dfs_by_year: dict, source_name="ons"):
        """
        Uploading dataframe in a GCP bucket using Cloud Run
        """
        existing_files = self.check_today_ingestion(source_name)
        if existing_files:
            return existing_files, False

        # upload date 
        now = datetime.now()
        current_year = int(now.strftime("%Y"))
        month = now.strftime("%m")
        day = now.strftime("%d")

        uploaded_files = []

        for data_year, df in dfs_by_year.items():
            file_name = f"ons_data_{data_year}.parquet"
            blob_path = f"raw/{source_name}/dt={day}-{month}-{current_year}/{file_name}"
            blob = self.bucket.blob(blob_path)

            if int(data_year) < current_year:
                if self.blob_exists(blob_path):
                    logger.info(f"{file_name} already exists on bucket. Skipping upload.")
                    continue

            df = df.astype(str)

            with BytesIO() as buffer:
                df.to_parquet(buffer, engine="pyarrow", index=False)
                buffer.seek(0)
                blob.upload_from_file(buffer, content_type="application/octet-stream")

            logger.info(f"File uploaded to gs://{self.bucket_name}/{blob_path}")
            uploaded_files.append(blob_path)

        return uploaded_files, True
    
    def query_bigquery(self, start_date: str, end_date: str, page: int, page_size: int):
        """
        Query data directily from BQ with pagination
        """

        start_date = self._normalize_date(start_date)
        end_date = self._normalize_date(end_date)
        client = bigquery.Client(project=self.project_id)

        table = f"{self.project_id}.{self.bq_dataset}.{self.table_ref}"

        # calculate pagination
        offset = (page - 1) * page_size

        query = f"""
        SELECT *
        FROM `{table}`
        WHERE ear_data BETWEEN @start_date AND @end_date
        ORDER BY ear_data
        LIMIT @page_size OFFSET @offset
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
                bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
                bigquery.ScalarQueryParameter("page_size", "INT64", page_size),
                bigquery.ScalarQueryParameter("offset", "INT64", offset),
            ]
        )

        df = client.query(query, job_config=job_config).to_dataframe()

        # também pegar o total de registros (sem paginação)
        count_query = f"""
        SELECT COUNT(*) as total
        FROM `{table}`
        WHERE ear_data BETWEEN @start_date AND @end_date
        """

        total_df = client.query(count_query, job_config=job_config).result().to_dataframe()
        total = int(total_df["total"].iloc[0])
        logger.info(f"BigQuery returned {len(df)} rows, total={total}")


        return df, total

    
    '''def load_to_bigquery(self, df: pd.DataFrame):
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

        logger.info(f"Data loaded on BigQuery: {table}")
        return table'''


