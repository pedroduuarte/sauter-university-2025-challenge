-- O código para criar a tabela externa.

CREATE OR REPLACE EXTERNAL TABLE `canvas-provider-472313-n5.reservatorios_externos_dataset.novos_dados_ons` 

WITH PARTITION COLUMNS 

OPTIONS (
 FORMAT = 'PARQUET',
 hive_partition_uri_prefix = 'gs://sauter-bucket-2025/raw/ons', 
 uris = ['gs://sauter-bucket-2025/raw/ons/*.parquet']
);
