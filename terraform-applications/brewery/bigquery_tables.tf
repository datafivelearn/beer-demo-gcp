resource "google_bigquery_table" "bq_table_breweries" {
    dataset_id = google_bigquery_dataset.bq_dataset_ahl.bq_dataset_beer
    table_id   = "breweries"
    schema = file("${path.module}/bigquery/tables/breweries.json")
    deletion_protection=false
    labels = {
        env = var.env
    }
    #range_partitioning {
    #    field = "season"
    #    range {
    #        start = 1950
    #        end = 2100
    #        interval = 1
    #    }
    #}
}