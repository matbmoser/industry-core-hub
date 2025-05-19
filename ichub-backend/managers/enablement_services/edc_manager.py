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

from uuid import UUID

from tractusx_sdk.dataspace.services import BaseEdcService
from tractusx_sdk.dataspace.models.connector.model_factory import ModelFactory
from managers.config.config_manager import ConfigManager

class EDCManager:
    """Manager for handling EDC (Eclipse Data Space Connector) related operations."""

    connector_version: str
    edc_controlplane_hostname: str
    edc_controlplane_management_api: str
    edc_service: BaseEdcService

    
    def __init__(self):
        self.connector_version = "v0_9_0"
        self.edc_controlplane_hostname = ConfigManager.get_config(
            "edc.controlplane.hostname"
        )
        self.edc_controlplane_management_api = ConfigManager.get_config(
            "edc.controlplane.managementpath"
        )
        self.edc_service = BaseEdcService(version=self.connector_version, base_url=self.edc_controlplane_management_api, dma_path=self.edc_controlplane_management_api)
        

    def register_submodel_asset(self, global_id: str, semantic_id: str, aas_id: UUID, submodel_id: UUID):
        """Register a submodel asset in the EDC."""
        # Implementation for registering a submodel asset
        print("=====================================")
        print("==== Eclipse Dataspace Connector ====")
        print("=====================================")
        print(f"Registering submodel asset with Global ID: {global_id}")
        print(f"Semantic ID: {semantic_id}")
        print(f"AAS ID: {aas_id}")
        print(f"Submodel ID: {submodel_id}")
        print("Submodel asset registered successfully (dummy implementation).")
        print()

    def register_or_get_submodel_bundle_asset(self, asset_id:str, base_url:str, semantic_id: str):
        """Register a submodel bundle asset in the EDC."""
        
        dct_type = "cx-taxo:SubmodelBundle"
        
        context =  {
            "edc": "https://w3id.org/edc/v0.0.1/ns/",
            "cx-common": "https://w3id.org/catenax/ontology/common#",
            "cx-taxo": "https://w3id.org/catenax/taxonomy#",
            "dct": "https://purl.org/dc/terms/",
            "aas-semantics": "https://admin-shell.io/aas/3/0/HasSemantics/"
        }

        data_address = { 
                "@type": "DataAddress",
                "type": "HttpData",
                "baseUrl": base_url,
                "proxyQueryParams": "false",
                "proxyPath": "true",
                "proxyMethod": "true"
            }
            
        asset = ModelFactory.get_asset_model(
            version=self.connector_version,
            context=context,
            oid=asset_id,
            properties={
                "dct:type": {
                    "@id": dct_type
                },
                "cx-common:version": "3.0",
                "aas-semantics:semanticId": {
                    "@id": semantic_id
                }
            },
            private_properties=None,
            data_address=data_address
        )
        
        response = self.edc_service.assets.create(obj=asset)
        
        print(response)
        
        # Implementation for registering a submodel bundle asset
        print("=====================================")
        print("==== Eclipse Dataspace Connector ====")
        print("=====================================")
        print(f"Registering submodel bundle asset with Semantic ID: {semantic_id}")
        print("Submodel bundle asset registered successfully (dummy implementation).")
        print()
