// Copyright 2023 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//    https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

resource "google_spanner_instance" "unified-data-spanner" {
  project          = var.project_id
  config           = var.spanner_config.location
  display_name     = var.spanner_config.instance_name
  processing_units = var.spanner_config.processing_units

  depends_on = [google_project_service.project]
}

resource "google_spanner_database" "database" {
  project                  = var.project_id
  instance                 = google_spanner_instance.unified-data-spanner.name
  name                     = var.spanner_config.db_name
  version_retention_period = "3d"
  ddl = [
    "CREATE TABLE Player (PlayerId STRING(MAX) NOT NULL,PlayerName STRING(MAX),PlayerAddress JSON,LastLogin TIMESTAMP) PRIMARY KEY(PlayerId)",

    "CREATE TABLE PlayerInventoryItem (PlayerId STRING(MAX) NOT NULL,ItemId STRING(MAX) NOT NULL,ItemName STRING(MAX) NOT NULL,Amount INT64,LastUpdate TIMESTAMP) PRIMARY KEY(PlayerId, ItemId),INTERLEAVE IN PARENT Player ON DELETE CASCADE",

    "CREATE TABLE GameTelemetry (eventId STRING(MAX),LastUpdated TIMESTAMP,PlayerId STRING(MAX) NOT NULL,PlayerName STRING(MAX),Event STRING(MAX)) PRIMARY KEY(eventId)",

    "CREATE TABLE StoreInventoryItem (ItemId STRING(MAX) NOT NULL,ItemName STRING(MAX) NOT NULL,PRICE FLOAT64,LastUpdate TIMESTAMP) PRIMARY KEY(ItemId)",

    "CREATE TABLE Venues (VenueId INT64 NOT NULL,VenueName STRING(1024),VenueAddress STRING(1024),VenueFeatures JSON,DateOpened DATE) PRIMARY KEY(VenueId)",
  ]
  deletion_protection = false
}
