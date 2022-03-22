
##########################################################################################
# Google BigQuery:  Data Set
##########################################################################################

resource "google_bigquery_dataset" "bq_dataset_beer" {
  dataset_id                  = "beer"
  friendly_name               = "beer"
  description                 = "Data set for beer demo"
  location                    = "US"
  #default_table_expiration_ms = 3600000

  labels = {
    env = var.env
    project = "beer demo"
  }
}
