
resource "random_string" "random" {
  length           = 36
  special          = true
  override_special = "!@#$%^&*"
}

locals {
    config_content = <<-EOT
        ["gcp"]
        database_private_ip_address="${google_sql_database_instance.postgresql.private_ip_address}"
        database_public_ip_address="${google_sql_database_instance.postgresql.public_ip_address}"
        postgres_instance_connection_name="${var.google_project_id}:${var.google_default_region}:${google_sql_database_instance.postgresql.name}"
        database_user_name="${google_sql_user.llmuser.name}"
        database_password_key="pgvector-password"
        image_upload_gcs_bucket="${module.gcs.names_list[0]}"
        google-project-id="${var.google_project_id}"
        cache-server-host = "${google_redis_instance.cache.host}"
        cache-server-port = 6379
        use-cache-server = "True"
        google-default-region = "${var.google_default_region}"
        api-key = "${random_string.random.result}"
    EOT
}

resource "local_file" "config-gcp" {
    filename = "../genai/examples/smart-npc/config.gcp.toml.template"
    content  = local.config_content
}

resource "null_resource" "generate_config_toml" {
  provisioner "local-exec" {
    # working_dir = "${path.root}"
    command = <<EOF
      cat "../genai/examples/smart-npc/config.gcp.toml.template" \
        "../genai/examples/smart-npc/config.app.toml.template" \
        > "../genai/examples/smart-npc/config.toml"
EOF
  }
  depends_on = [
    local_file.config-gcp
  ]
}

resource "null_resource" "generate_config_yaml" {
  provisioner "local-exec" {
    command = <<EOF
kubectl create configmap \
  --dry-run=client smart-npc-config --from-file=../genai/examples/smart-npc/config.toml \
  --output yaml | tee "../genai/examples/smart-npc/config.yaml"
EOF
  }
  depends_on = [
    null_resource.generate_config_toml
  ]
}