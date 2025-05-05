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


# Package-level variables
__author__ = 'Eclipse Tractus-X Contributors'
__license__ = "Apache License, Version 2.0"

from typing import Dict
from uuid import UUID

class DTRManager:
    
    def __init__(self, dtr_url: str = 'http://localhost:8443', dtr_username: str = 'username', dtr_password: str = 'password'):
        self.dtr_url = dtr_url
        self.dtr_username = dtr_username
        self.dtr_password = dtr_password
        self.dtr_client = None


    def register_twin(self, global_id: UUID, aas_id: UUID, manufacturer_id: str, manufacturer_part_id: str,
                      customer_part_ids: Dict[str, str], part_category: str):
        """
        Registers a twin in the DTR.
        """
        print(f"Registering twin with global_id={global_id}, aas_id={aas_id}, "
              f"manufacturer_id={manufacturer_id}, manufacturer_part_id={manufacturer_part_id}, "
              f"customer_part_ids={customer_part_ids}, part_category={part_category}")

        pass