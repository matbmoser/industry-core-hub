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

from typing import Optional, Dict, Any
from uuid import UUID

from managers.metadata_database.manager import RepositoryManagerFactory, RepositoryManager
from managers.enablement_services.dtr_manager import DTRManager
from managers.enablement_services.edc_manager import EDCManager
from managers.enablement_services.submodel_service_manager import SubmodelServiceManager
from models.services.twin_management import CatalogPartTwinCreate, TwinRead, TwinDetailsRead, TwinAspectCreate, TwinAspectRead
from models.services.part_management import CatalogPartBase

class TwinManagementService:
    """
    Service class for managing twin-related operations (CRUD and Twin sharing).
    """

    def __init__(self, ):
        self._repositories: RepositoryManager = RepositoryManagerFactory.create()
        self._edc_manager: EDCManager = EDCManager()
        self._submodel_service_manager: SubmodelServiceManager = SubmodelServiceManager()

    def create_catalog_part_twin(self, create_input: CatalogPartTwinCreate, enablement_service_stack_name: str = 'EDC/DTR Default') -> TwinRead:
        with self._repositories as repo:
            # Step 1: Retrieve the catalog part entity according to the catalog part data (manufacturer_id, manufacturer_part_id)
            db_catalog_parts = repo.catalog_part_repository.find_by_manufacturer_id_manufacturer_part_id(
                create_input.manufacturer_id,
                create_input.manufacturer_part_id,
                join_partner_catalog_parts=True
            )
            if not db_catalog_parts:
                raise ValueError("Catalog part not found.")
            else:
                db_catalog_part = db_catalog_parts[0]

            # Step 2: Retrieve the enablement service stack entity from the DB according to the given name
            # (if not there => raise error)
            db_enablement_service_stack = repo.enablement_service_stack_repository.get_by_name(
                enablement_service_stack_name
            )
            if not db_enablement_service_stack:
                raise ValueError(f"Enablement service stack '{enablement_service_stack_name}' not found.")

            # Step 3a: Load existing twin metadata from the DB (if there)
            if db_catalog_part.twin_id:
                db_twin = repo.twin_repository.find_by_id(db_catalog_part.twin_id)
                if not db_twin:
                    raise ValueError("Twin not found.")
            # Step 3b: If no twin was there, create it now in the DB (generating on demand a new global_id and dtr_aas_id)
            else:
                db_twin = repo.twin_repository.create_new(
                    global_id=create_input.global_id,
                    dtr_aas_id=create_input.dtr_aas_id)
                repo.commit()
                repo.refresh(db_twin)

                db_catalog_part.twin_id = db_twin.id
                repo.commit()

            # Step 4: Try to find the twin registration for the twin id and enablement service stack id
            # (if not there => create it now, setting the dtr_registered flag to False)
            db_twin_registration = repo.twin_registration_repository.get_by_twin_id_enablement_service_stack_id(
                db_twin.id,
                db_enablement_service_stack.id
            )
            if not db_twin_registration:
                db_twin_registration = repo.twin_registration_repository.create_new(
                    twin_id=db_twin.id,
                    enablement_service_stack_id=db_enablement_service_stack.id
                )
                repo.commit()

            # Step 6: Check the dtr_registered flag on the twin registration entity
            # (if True => we can skip the operation from here on => nothing to do)
            # (if False => we need to register the twin in the DTR using the industry core SDK, then
            #  update the twin registration entity with the dtr_registered flag to True)
            if not db_twin_registration.dtr_registered:
                dtr_manager = _create_dtr_manager(db_enablement_service_stack.connection_settings)
                
                customer_part_ids = {partner_catalog_part.customer_part_id: partner_catalog_part.business_partner.bpnl 
                                      for partner_catalog_part in db_catalog_part.partner_catalog_parts}
                
                dtr_manager.register_twin(
                    global_id=db_twin.global_id,
                    aas_id=db_twin.aas_id,
                    manufacturer_id=create_input.manufacturer_id,
                    manufacturer_part_id=create_input.manufacturer_part_id,
                    customer_part_ids=customer_part_ids,
                    part_category=db_catalog_part.category
                )

                db_twin_registration.dtr_registered = True

            return TwinRead(
                globalId=db_twin.global_id,
                dtrAasId=db_twin.aas_id,
                createdDate=db_twin.created_date,
                modifiedDate=db_twin.modified_date
            )

    def create_catalog_part_twin_share(self, catalog_part_input: CatalogPartBase, business_partner_name: str) -> bool:
        
        with self._repositories as repo:
            # Step 1: Retrieve the catalog part entity according to the catalog part data (manufacturer_id, manufacturer_part_id)
            db_catalog_parts = repo.catalog_part_repository.find_by_manufacturer_id_manufacturer_part_id(
                catalog_part_input.manufacturer_id,
                catalog_part_input.manufacturer_part_id,
                join_partner_catalog_parts=True
            )
            if not db_catalog_parts:
                raise ValueError("Catalog part not found.")
            db_catalog_part = db_catalog_parts[0]

            # Step 2: Retrieve the business partner entity according to the business_partner_name
            # (if not there => raise error)
            db_business_partner = repo.business_partner_repository.get_by_name(business_partner_name)
            if not db_business_partner:
                raise ValueError(f"Business partner '{business_partner_name}' not found.")

            # Step 3a: Consistency check if there is a twin associated with the catalog part
            if not db_catalog_part.twin_id:
                raise ValueError("Catalog part has not yet a twin associated.")
            # Step 3b: Consistency check if there exists a partner catalog part entity for the given catalog part and business partner
            if not db_catalog_part.find_partner_catalog_part_by_business_partner_name(business_partner_name):
                raise ValueError(f"Not customer part ID existing for given business partner '{business_partner_name}'.")

            # Step 4: Retrieve the twin entity for the catalog part entity
            db_twin = repo.twin_repository.find_by_id(db_catalog_part.twin_id)
            if not db_twin:
                raise ValueError("Twin not found.")

            # Step 5: Retrieve the first data exchange agreement entity for the business partner
            # (this will will later be replaced with an explicit mechanism choose a specific data exchange agreement)
            db_data_exchange_agreements = repo.data_exchange_agreement_repository.get_by_business_partner_id(
                db_business_partner.id
            )
            if not db_data_exchange_agreements:
                raise ValueError(f"No data exchange agreement found for business partner '{business_partner_name}'.")
            db_data_exchange_agreement = db_data_exchange_agreements[0] # Get the first one for now
            
            # Step 6: Check if there is already a twin exchange entity for the twin and data exchange agreement and create it if not
            db_twin_exchange = repo.twin_exchange_repository.get_by_twin_id_data_exchange_agreement_id(
                db_twin.id,
                db_data_exchange_agreement.id
            )
            if not db_twin_exchange:
                db_twin_exchange = repo.twin_exchange_repository.create_new(
                    twin_id=db_twin.id,
                    data_exchange_agreement_id=db_data_exchange_agreement.id
                )
                repo.commit()
                return True
            else:
                return False

    def create_twin_aspect(self, twin_aspect_create: TwinAspectCreate) -> TwinAspectRead:
        """
        Create a new twin aspect for a give twin.
        """

        with self._repositories as repo:
            
            # Step 1: Retrieve the twin entity according to the global_id
            db_twin = repo.twin_repository.find_by_global_id(twin_aspect_create.global_id)
            if not db_twin:
                raise ValueError(f"Twin for global ID '{twin_aspect_create.global_id}' not found.")

            # Step 2: Retrieve a potentially existing twin aspect entity for the given twin_id and semantic_id
            # (if there => for the moment we could raise an error; but in the future I recommend
            #  the API to be "repeatable" - e.g. to update the payload in the submodel service)

        # Step 3: Create the twin aspect entity in the database
        # (generate a new submodel_id for it if not given)
        # Step 3a: Create a twin aspect registration entry pointing to the singleton enablement service stack
        # (set the status to PLANNED and the mode to SINGLE)

        # Step 4: Upload the payload to the submodel service
        # (use industry core SDK or it's wrapper for that)
        # Step 4a: Update the twin aspect registration entry with the status to STORED

        # Step 5: (later to be implemented): Register the aspect as asset in the EDC (if necessary)
        # (use industry core SDK or it's wrapper for that)
        # Step 5a: Update the twin aspect registration entry with the status to EDC_REGISTERED

        # Step 6: Attach a submodel descriptor to the shell descriptor in the DTR
        # (use industry core SDK or it's wrapper for that)
        # Step 6a: Update the twin aspect registration entry with the status to DTR_REGISTERED
        # (tricky: use the right asset ID for the EDC and the right URLs for data plane and control plane)

        pass

    def get_twin_details(self, global_id: UUID) -> TwinDetailsRead:
        pass


def _create_dtr_manager(connection_settings: Optional[Dict[str, Any]]) -> DTRManager:
    """
    Create a new instance of the DTRManager class.
    """
    # TODO: later we can configure the manager via the connection settings from the DB here

    return DTRManager()

