#################################################################################
# Eclipse Tractus-X - Industry Core Hub Backend
#
# Copyright (c) 2025 DRÄXLMAIER Group
# (represented by Lisa Dräxlmaier GmbH)
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

from typing import List, Optional

from fastapi import FastAPI

from services.part_management_service import PartManagementService
from services.partner_management_service import PartnerManagementService
from services.twin_management_service import TwinManagementService
from models.services.part_management import CatalogPartRead, PartnerCatalogPartBase
from models.services.partner_management import BusinessPartnerRead, BusinessPartnerCreate, BusinessPartnerCreateInput, DataExchangeAgreementRead
from models.services.twin_management import TwinCreateBase, CatalogPartTwinCreate, TwinRead

app = FastAPI(title="Industry Core Hub Backend API", version="0.0.1")

part_management_service = PartManagementService()
partner_management_service = PartnerManagementService()
twin_management_service = TwinManagementService()

@app.get("/part-management/catalog-part/{manufacturer_id}/{manufacturer_part_id}", response_model=CatalogPartRead)
async def part_management_get_catalog_part(manufacturer_id: str, manufacturer_part_id: str) -> Optional[CatalogPartRead]:
    return part_management_service.get_catalog_part(manufacturer_id, manufacturer_part_id)

@app.get("/part-management/catalog-part", response_model=List[CatalogPartRead])
async def part_management_get_catalog_parts() -> List[CatalogPartRead]:
    return part_management_service.get_catalog_parts()

@app.post("/part-management/catalog-part/{manufacturer_id}/{manufacturer_part_id}", response_model=CatalogPartRead)
async def part_management_create_catalog_part(manufacturer_id: str, manufacturer_part_id: str, customer_parts: Optional[List[PartnerCatalogPartBase]]) -> CatalogPartRead:
    return part_management_service.create_catalog_part_by_ids(manufacturer_id, manufacturer_part_id, customer_parts)

@app.get("/partner-management/business-partner", response_model=List[BusinessPartnerRead])
async def partner_management_get_business_partners() -> List[BusinessPartnerRead]:
    return partner_management_service.list_business_partners()

@app.get("/partner-management/business-partner/{business_partner_name}", response_model=Optional[BusinessPartnerRead])
async def partner_management_get_business_partner(business_partner_name: str) -> Optional[BusinessPartnerRead]:
    return partner_management_service.get_business_partner(business_partner_name)

@app.post("/partner-management/business-partner/{business_partner_name}", response_model=BusinessPartnerRead)
async def partner_management_create_business_partner(business_partner_name: str, create_input: BusinessPartnerCreateInput) -> BusinessPartnerRead:
    return partner_management_service.create_business_partner(BusinessPartnerCreate(
        name=business_partner_name,
        bpnl=create_input.bpnl
    ))

@app.get("/partner-management/business-partner/{business_partner_name}/data-exchange-agreement", response_model=List[DataExchangeAgreementRead])
async def partner_management_get_data_exchange_agreements(business_partner_name: str) -> List[DataExchangeAgreementRead]:
    return partner_management_service.get_data_exchange_agreements(business_partner_name)

@app.post("/twin-management/catalog-part-twin/{manufacturer_id}/{manufacturer_part_id}", response_model=TwinRead)
async def twin_management_create_catalog_part_twin(manufacturer_id: str, manufacturer_part_id: str, twin_create: TwinCreateBase) -> TwinRead:
    catalog_part_twin_create = CatalogPartTwinCreate(
        manufacturerId=manufacturer_id,
        manufacturerPartId=manufacturer_part_id,
        globalId=twin_create.global_id,
        dtrAasId=twin_create.dtr_aas_id
    )
    return twin_management_service.create_catalog_part_twin(catalog_part_twin_create)
