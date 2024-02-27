resource "google_sql_database_instance" "database" {
  project     = var.gcp_project_id
  name        = "database-instance"
  region      = var.gcp_region
  database_version = "POSTGRES_13"
  deletion_protection = false

  # min tier
  settings {
    tier = "db-f1-micro"
  }
  
    depends_on = [module.enable_google_apis]
}

resource "google_sql_database" "database" {
  name     = "database"
  instance = google_sql_database_instance.database.name
  project  = var.gcp_project_id
}

output "connection_name" {
  value = google_sql_database_instance.database.name
}

resource "google_sql_user" "database_user" {
  name     = "user"
  instance = google_sql_database_instance.database.name
  password = "password"
  project  = var.gcp_project_id
}

