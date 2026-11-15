# Dataset Camada Bronze

resource "google_bigquery_dataset" "bronze" {
  dataset_id  = local.config.bigquery.datasets.bronze
  description = "Camada Bronze - Dados brutos do PNCP"
  location    = local.config.bigquery.location

  delete_contents_on_destroy      = true
  default_table_expiration_ms     = 4320000000
  default_partition_expiration_ms = 4320000000

}

# Dataset Camada Silver
resource "google_bigquery_dataset" "silver" {
  dataset_id                      = local.config.bigquery.datasets.silver
  description                     = "Camada Silver - Dados transformados do PNCP"
  location                        = local.config.bigquery.location
  delete_contents_on_destroy      = true
  default_table_expiration_ms     = 4320000000
  default_partition_expiration_ms = 4320000000

}

# Dataset Camada Gold

resource "google_bigquery_dataset" "gold" {
  dataset_id                      = local.config.bigquery.datasets.gold
  description                     = "Camada Gold: Modelos dimensionais e indicadores analíticos (dbt marts)"
  location                        = local.config.bigquery.location
  delete_contents_on_destroy      = true
  default_table_expiration_ms     = 4320000000
  default_partition_expiration_ms = 4320000000
}
