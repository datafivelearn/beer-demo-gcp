module "function_beer_demo_pipelines" {
  source = "../modules/function"

  gcp_project_id = var.gcp_project_id
  function_name = "beer_demo_data_pipeline"
  function_description = "Data pipeline to get brewery data and load to BigQuery"
  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
  function_entry_point = "get_data"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = 128
  #function_trigger_http = null
  function_event_trigger_resource = google_pubsub_topic.beer_demo_topic.name # this function gets triggered when an event is added to the beer demo pubsub topic
}
