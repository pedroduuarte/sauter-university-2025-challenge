resource "google_bigquery_dataset" "onsDataset" {

  dataset_id                  = var.dataset_id
  friendly_name               = var.friendly_name
  location                    = var.location-big-query
  default_table_expiration_ms = var.default_table_expiration_ms

  labels = var.labels
}

resource "google_bigquery_table" "reservatoriosExternos" {
  dataset_id = google_bigquery_dataset.onsDataset.dataset_id
  table_id   = var.table_id

  labels = var.labels

    external_data_configuration {
    autodetect    = true
    source_format = var.source_format


    source_uris = var.source_uris
    }
 }