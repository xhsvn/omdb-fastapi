locals {
  image = var.container_image != "" ? var.container_image : "${google_artifact_registry_repository.repository.location}-docker.pkg.dev/${var.gcp_project_id}/${google_artifact_registry_repository.repository.name}/${var.app_name}:latest"
}

resource "google_cloud_run_v2_service" "api" {
  name     = "${var.app_name}-api"
  location = var.gcp_region
  ingress  = "INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER"

  template {
    scaling {
      min_instance_count = 0
      max_instance_count = 3
    }
    volumes {
      name = "cloudsql"
      cloud_sql_instance {
        instances = [google_sql_database_instance.database.connection_name]
      }
    }
    service_account = google_service_account.app.email

    containers {
      image   = local.image
      command = var.container_command_api
      resources {
        limits = {
          cpu    = "1000m"
          memory = "1Gi"
        }
        cpu_idle = true
      }
      volume_mounts {
        name       = "cloudsql"
        mount_path = "/cloudsql"
      }
      env {
        name  = "GOOGLE_PROJECT_ID"
        value = var.gcp_project_id
      }
      env {
        name  = "PUBSUB_MOVIES_FETCH_TOPIC"
        value = google_pubsub_topic.main.name
      }
      env {
        name  = "POSTGRES_CONNECTION_NAME"
        value = google_sql_database_instance.database.connection_name
      }
      env {
        name  = "POSTGRES_DB"
        value = google_sql_database.database.name
      }
      env {
        name  = "POSTGRES_USER"
        value = google_sql_user.database_user.name
      }
      env {
        name  = "POSTGRES_PASSWORD"
        value = google_sql_user.database_user.password
      }
      env {
        name  = "OMDB_API_KEY"
        value = "3ea4bc11"

      }
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }

  depends_on = [module.enable_google_apis, google_sql_database_instance.database, google_pubsub_subscription.main]
}

resource "google_cloud_run_v2_service" "worker" {
  name     = "${var.app_name}-worker"
  location = var.gcp_region
  ingress  = "INGRESS_TRAFFIC_INTERNAL_ONLY"

  template {
    scaling {
      min_instance_count = 0
      max_instance_count = 1
    }

    volumes {
      name = "cloudsql"
      cloud_sql_instance {
        instances = [google_sql_database_instance.database.connection_name]
      }
    }

    service_account = google_service_account.app.email

    containers {
      image   = local.image
      command = var.container_command_worker
      resources {
        limits = {
          cpu    = "1000m"
          memory = "4Gi"
        }
        cpu_idle = true
      }
      volume_mounts {
        name       = "cloudsql"
        mount_path = "/cloudsql"
      }
      env {
        name  = "GOOGLE_PROJECT_ID"
        value = var.gcp_project_id
      }
      env {
        name  = "PUBSUB_MOVIES_FETCH_TOPIC"
        value = google_pubsub_topic.main.name
      }
      env {
        name  = "POSTGRES_CONNECTION_NAME"
        value = google_sql_database_instance.database.connection_name
      }
      env {
        name  = "POSTGRES_DB"
        value = google_sql_database.database.name
      }
      env {
        name  = "POSTGRES_USER"
        value = google_sql_user.database_user.name
      }
      env {
        name  = "POSTGRES_PASSWORD"
        value = google_sql_user.database_user.password
      }
      env {
        name  = "OMDB_API_KEY"
        value = "3ea4bc11"
      }
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }

  depends_on = [module.enable_google_apis, google_sql_database_instance.database]
}

resource "google_cloud_run_service_iam_member" "api_invoker" {
  location = google_cloud_run_v2_service.api.location
  project  = google_cloud_run_v2_service.api.project
  service  = google_cloud_run_v2_service.api.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

resource "google_cloud_run_service_iam_member" "worker_invoker" {
  location = google_cloud_run_v2_service.worker.location
  project  = google_cloud_run_v2_service.worker.project
  service  = google_cloud_run_v2_service.worker.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.pubsub.email}"
}


resource "google_project_iam_member" "sql_connect" {
  for_each = toset([
    "roles/cloudsql.client",
    "roles/cloudsql.editor",
    "roles/cloudsql.admin",
    "roles/resourcemanager.projectIamAdmin"
  ])
  role    = each.key
  project = google_sql_database_instance.database.project
  member  = "serviceAccount:${google_service_account.app.email}"
}
