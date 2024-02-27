resource "google_pubsub_topic" "main" {
  name = var.app_name

  depends_on = [module.enable_google_apis]
}

resource "google_pubsub_topic" "main_dead_letter" {
  name = "${google_pubsub_topic.main.name}-dlq"

  depends_on = [module.enable_google_apis]
}

resource "google_pubsub_subscription" "main" {
  name  = "${var.app_name}-subscription"
  topic = google_pubsub_topic.main.name

  ack_deadline_seconds = 600

  message_retention_duration = "600s"

  expiration_policy {
    ttl = ""
  }
  retry_policy {
    minimum_backoff = "15s"
  }

  enable_message_ordering = false

  dead_letter_policy {
    dead_letter_topic     = google_pubsub_topic.main_dead_letter.id
    max_delivery_attempts = 5
  }

  push_config {
    push_endpoint = "${google_cloud_run_v2_service.worker.uri}${var.worker_subscription_url_path}"
    oidc_token {
      service_account_email = google_service_account.pubsub.email
    }
    attributes = {
      x-goog-version = "v1"
    }
  }
}

resource "google_pubsub_subscription" "main_dead_letter" {
  name  = "${google_pubsub_subscription.main.name}-dlq"
  topic = google_pubsub_topic.main_dead_letter.name

  ack_deadline_seconds = 600

  message_retention_duration = "600s"

  expiration_policy {
    ttl = ""
  }
  retry_policy {
    minimum_backoff = "15s"
  }

  enable_message_ordering = false

  push_config {
    push_endpoint = "${google_cloud_run_v2_service.worker.uri}${var.worker_subscription_dead_letter_url_path}"
    oidc_token {
      service_account_email = google_service_account.pubsub.email
    }
    attributes = {
      x-goog-version = "v1"
    }
  }
}

resource "google_pubsub_subscription_iam_member" "subscription_subscriber_role" {
  subscription = google_pubsub_subscription.main.name
  role         = "roles/pubsub.subscriber"
  member       = "serviceAccount:${google_service_account.app.email}"
}

resource "google_pubsub_topic_iam_member" "topic_publisher_role" {
  topic  = google_pubsub_topic.main.name
  role   = "roles/pubsub.publisher"
  member = "serviceAccount:${google_service_account.app.email}"
}
