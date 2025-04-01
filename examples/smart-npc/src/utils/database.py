# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Database connection Wrapper

Wrapper of database operations.
"""

import sqlalchemy

from google.cloud import secretmanager
from google.cloud.sql.connector import Connector

class DataConnection:
    """
    Wraps the database connection.
    """
    def __get_db_password(self) -> str:
        """Get database user's password from secret manager.

        Returns:
            Password.
        """
        if self.database_password is not None:
            return self.database_password

        if self.config["gcp"]["google-project-id"] == "":
            raise ValueError("google-project-id not set in config-secrets.toml")

        client = secretmanager.SecretManagerServiceClient()

        request = secretmanager.AccessSecretVersionRequest(
            name=f"projects/{self.config['gcp']['google-project-id']}/secrets/{self.config['gcp']['database_password_key']}/versions/latest",  # pylint: disable=line-too-long, inconsistent-quotes
        )
        response = client.access_secret_version(request)

        payload = response.payload.data.decode("UTF-8")
        self.database_password = payload
        return self.database_password

    def __init__(self, config):
        """Initialize the DataConnection object

        Args:
            config (dict): Database configuration object.
        """
        self.config = config
        self.connector = Connector()
        self.database_password = None
        self.__pool = None

    def __getconn(self):
        """Opens the connetion to the database.

        Returns:
            Connection object.
        """
        conn = self.connector.connect(
            self.config["gcp"]["postgres_instance_connection_name"],
            "pg8000",
            user=self.config["gcp"]["database_user_name"],
            password=self.__get_db_password(),
            db="postgres",
        )

        return conn

    def execute(self, sql:str, sql_params:dict) -> any:
        """Execute SQL query and returns the results.

        Args:
            sql (str): SQL query.
            sql_params (dict): SQL parameters.

        Returns:
            Query result.
        """
        if self.__pool is None:
            self.__pool = sqlalchemy.create_engine(
                    "postgresql+pg8000://",
                    creator=self.__getconn,
                )

        with self.__pool.connect() as db_conn:
            rows = db_conn.execute(sqlalchemy.text(sql), sql_params)
            db_conn.commit()
            return rows
