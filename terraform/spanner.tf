resource "google_spanner_instance" "npc-chat" {
  name             = "npc-chat"
  display_name     = "Data behind npc-chat-api"
  config           = "regional-us-central1"
  autoscaling_config {
    autoscaling_limits {
      max_processing_units            = 10000
      min_processing_units            = 1000
    }
    autoscaling_targets {
      high_priority_cpu_utilization_percent = 75
      storage_utilization_percent           = 90
    }
  }
}

resource "google_spanner_database" "npc-chat" {
  instance = google_spanner_instance.npc-chat.name
  name     = "npc-chat"
  version_retention_period = "3d"
  ddl = [<<-EOT
    CREATE TABLE EntityHistoryBase (
        EntityId INT64,
        IsWorldData bool,
        EventId INT64,
        EntityName STRING(MAX),
        EntityType INT64,
        EventDescription STRING(MAX),
        EventDescriptionEmbedding ARRAY<FLOAT64>,
    ) PRIMARY KEY(EntityId, IsWorldData, EventId)
  EOT
  , <<-EOT
    CREATE TABLE EntityHistoryDynamic (
        EntityId INT64,
        EventTime TIMESTAMP OPTIONS (
            allow_commit_timestamp = true
        ),
        MessageId INT64,
        EntityName STRING(MAX),
        EntityType INT64,
        TargetEntityId INT64,
        TargetEntityName STRING(MAX),
        EventDescription STRING(MAX),
        EventDescriptionEmbedding ARRAY<FLOAT64>,
    ) PRIMARY KEY(EntityId, EventTime DESC, MessageId DESC)
  EOT
  , <<-EOT
    CREATE INDEX EntityHistoryDynamicByEntityAndTarget
    ON EntityHistoryDynamic(EntityId, TargetEntityId, EventTime DESC, MessageId DESC)
    STORING (EntityName, TargetEntityName, EventDescription, EventDescriptionEmbedding)
  EOT
  , <<-EOT
    CREATE INDEX EntityHistoryDynamicByTarget
    ON EntityHistoryDynamic(TargetEntityId, EventTime DESC, MessageId DESC)
    STORING (EntityName, TargetEntityName, EventDescription, EventDescriptionEmbedding)
  EOT
  ]
}
