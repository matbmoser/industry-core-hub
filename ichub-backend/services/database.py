#################################################################################
# Eclipse Tractus-X - Industry Core Hub Backend
#
# Copyright (c) 2025 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the
# License for the specific language govern in permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0
#################################################################################

from config.config_manager import ConfigManager
from config.log_manager import LoggingManager
from typing import Generator
from sqlmodel import Session, SQLModel, create_engine

connection_string = ConfigManager.get_config("database.connection_string", default={})
db_echo = ConfigManager.get_config("database.echo", default={False})

engine = create_engine(str(connection_string), echo=db_echo)

logger = LoggingManager.get_logger(__name__)

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

def connect_and_test():
    try:
        with engine.connect() as _:
            pass
        logger.info("Database connection established successfully.")
    except Exception as e:
        logger.critical(f"Failed to establish database connection: {e}")
        raise

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session