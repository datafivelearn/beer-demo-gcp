GCP Function Terraform Module
===========

A terraform module to provide a <resource name> in AWS/AZURE/ETC,ETC.

This should be used an a generic template to be included in every terraform module.

Module Input Variables
----------------------

- `gcp_project_id` - The Google Cloud Project id
- `function_name` - Name of the function
- `function_description` - Description of the function
- `function_deployment_bucket_name` - Name of the bucket where zips are loaded to
- `function_entry_point` - Name of primary function that will get called with GCP Function triggered
- `function_region` - GCP region of function to deploy to
- `function_runtime` - Language and version - valid values = [python37, python38, python39]
- `function_available_memory_mb` - Available memory in mb for function
- `function_timeout` - Function timeout in seconds
- `function_trigger_http` - trigger function via http
- `function_event_trigger_resource` - Name of the resouce that triggers function


Usage
-----

```hcl
module "gpc-function-example-http-triggered" {
  source = "../modules/function"
  gcp_project_id = var.gcp_project_id
  function_name = "gpc-function-example-http-triggered"
  function_description = "example function with http trigger"
  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
  function_entry_point = "main"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = 128
  function_timeout = 600
  function_trigger_http = true
  #function_event_trigger_resource = none - commented out
}

module "gpc-function-example-pubsubtopic-triggered" {
  source = "../modules/function"
  gcp_project_id = var.gcp_project_id
  function_name = "gpc-function-example-pubsubtopic-triggered"
  function_description = "example function triggered from a pub/sub topic"
  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
  function_entry_point = "main"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = 128
  function_timeout = 540
  #function_trigger_http = commented out
  function_event_trigger_resource = google_pubsub_topic.topic_that_triggers.name
}

```

Authors
=======

high5technologies@company.com