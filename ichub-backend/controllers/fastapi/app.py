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

from pydantic import BaseModel, Field

from fastapi import FastAPI, HTTPException

from services.part_management_service import PartManagementService
from services.partner_management_service import PartnerManagementService
from services.twin_management_service import TwinManagementService
from models.services.part_management import CatalogPartBase, CatalogPartRead, CatalogPartCreate
from models.services.partner_management import BusinessPartnerRead, BusinessPartnerCreate, DataExchangeAgreementRead
from models.services.twin_management import TwinRead, TwinCreateBase, CatalogPartTwinCreate

tags_metadata = [
    {
        "name": "Part Management",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed ..."
    },
    {
        "name": "Partner Management",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed ..."
    },
    {
        "name": "Twin Management",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed ..."
    }
]

app = FastAPI(title="Industry Core Hub Backend API", version="0.0.1", openapi_tags=tags_metadata)

part_management_service = PartManagementService()
partner_management_service = PartnerManagementService()
twin_management_service = TwinManagementService()

class BusinessPartnerNameWrapper(BaseModel):
    business_partner_name: str = Field(alias="businessPartnerName", description="Name of the business partner") 

@app.get("/part-management/catalog-part/{manufacturer_id}/{manufacturer_part_id}", response_model=CatalogPartRead, tags=["Part Management"])
async def part_management_get_catalog_part(manufacturer_id: str, manufacturer_part_id: str) -> Optional[CatalogPartRead]:
    return part_management_service.get_catalog_part(manufacturer_id, manufacturer_part_id)

@app.get("/part-management/catalog-part", response_model=List[CatalogPartRead], tags=["Part Management"])
async def part_management_get_catalog_parts() -> List[CatalogPartRead]:
    return part_management_service.get_catalog_parts()

@app.post("/part-management/catalog-part", response_model=CatalogPartRead, tags=["Part Management"])
async def part_management_create_catalog_part(catalog_part_create: CatalogPartCreate) -> CatalogPartRead:
    return part_management_service.create_catalog_part(catalog_part_create)

@app.get("/partner-management/business-partner", response_model=List[BusinessPartnerRead], tags=["Partner Management"])
async def partner_management_get_business_partners() -> List[BusinessPartnerRead]:
    return partner_management_service.list_business_partners()

@app.get("/partner-management/business-partner/{business_partner_number}", response_model=Optional[BusinessPartnerRead], tags=["Partner Management"])
async def partner_management_get_business_partner(business_partner_number: str) -> Optional[BusinessPartnerRead]:
    return partner_management_service.get_business_partner(business_partner_number)

@app.post("/partner-management/business-partner", response_model=BusinessPartnerRead, tags=["Partner Management"])
async def partner_management_create_business_partner(business_partner_create: BusinessPartnerCreate) -> BusinessPartnerRead:
    return partner_management_service.create_business_partner(business_partner_create)

@app.get("/partner-management/business-partner/{business_partner_number}/data-exchange-agreement", response_model=List[DataExchangeAgreementRead], tags=["Partner Management"])
async def partner_management_get_data_exchange_agreements(business_partner_number: str) -> List[DataExchangeAgreementRead]:
    return partner_management_service.get_data_exchange_agreements(business_partner_number)

@app.post("/twin-management/catalog-part-twin/{manufacturer_id}/{manufacturer_part_id}", response_model=TwinRead, tags=["Twin Management"])
async def twin_management_create_catalog_part_twin(manufacturer_id: str, manufacturer_part_id: str, twin_create: TwinCreateBase) -> TwinRead:
    catalog_part_twin_create = CatalogPartTwinCreate(
        manufacturerId=manufacturer_id,
        manufacturerPartId=manufacturer_part_id,
        globalId=twin_create.global_id,
        dtrAasId=twin_create.dtr_aas_id
    )
    return twin_management_service.create_catalog_part_twin(catalog_part_twin_create)

@app.post("/twin-management/catalog-part-twin/{manufacturer_id}/{manufacturer_part_id}/share", responses={
    201: {"description": "Catalog part twin shared successfully"},
    204: {"description": "Catalog part twin already shared"}
}, tags=["Twin Management"])
async def twin_management_share_catalog_part_twin(manufacturer_id: str, manufacturer_part_id: str, business_partner_name: BusinessPartnerNameWrapper):
    catalog_part_input = CatalogPartBase(manufacturerId=manufacturer_id, manufacturerPartId=manufacturer_part_id)
    
    if twin_management_service.create_catalog_part_twin_share(catalog_part_input, business_partner_name.business_partner_name):
        raise HTTPException(status_code=201, detail="Catalog part twin shared successfully")    
    else:
        raise HTTPException(status_code=204, detail="Catalog part twin already shared")
