terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

locals {
  config = yamldecode(file("${path.module}/../config/config.yaml"))
}

provider "google" {
  project = "pncp-project"
  region  = local.config.bigquery.location

}
