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

from uuid import UUID

from managers.metadata_database.manager import RepositoryManagerFactory
from models.services.twin_management import CatalogPartTwinCreate, TwinRead, TwinDetailsRead, TwinAspectCreate, TwinAspectRead


class TwinManagementService:
    """
    Service class for managing twin-related operations (CRUD and Twin sharing).
    """

    def __init__(self, ):
        self.repositories = RepositoryManagerFactory.create()

    def create_catalog_part_twin(self, create_input: CatalogPartTwinCreate) -> TwinRead:
        with self.repositories as repo:
            # Step 1: Retrieve the catalog part entity according to the catalog part data (manufacturer_id, manufacturer_part_id)
            db_catalog_parts = repo.catalog_part_repository.find_by_manufacturer_id_manufacturer_part_id(
                create_input.manufacturer_id,
                create_input.manufacturer_part_id
            )
            if not db_catalog_parts:
                raise ValueError("Catalog part not found.")
            else:
                db_catalog_part = db_catalog_parts[0]

            # Step 2 (future): Retrieve the enablement service stack entity from the DB according to the given name
            # (for the moment: we have a singleton entity for that - e.g. with id 1)
            # (if not there => raise error)
            db_enablement_service_stack = repo.enablement_service_stack_repository.find_all(limit=1)[0]

            # Step 3: Check the twin_id field of that entity if a twin is already registered
            if db_catalog_part.twin_id:
                raise ValueError("Twin already registered for this catalog part.")

            # Step 4: If no twin was there, create it now in the DB (generating on demand a new global_id and dtr_aas_id)
            db_twin = repo.twin_repository.create_new(
                global_id=create_input.global_id,
                dtr_aas_id=create_input.dtr_aas_id)
            repo.commit()
            repo.refresh(db_twin)

            # Step 4a: Update the catalog part entity with the twin_id
            db_catalog_part.twin_id = db_twin.id
            repo.commit()

            # Step 5: Try to find the twin registration for the twin id and enablement service stack id
            # (if not there => create it now, setting the dtr_registered flag to False)
        
            # Step 6: Check the dtr_registered flag on the twin registration entity
            # (if True => we can skip the operation from here on => nothing to do)
            # (if False => we need to register the twin in the DTR using the industry core SDK, then
            #  update the twin registration entity with the dtr_registered flag to True)
            return TwinRead(
                globalId=db_twin.global_id,
                dtrAasId=db_twin.aas_id,
                createdDate=db_twin.created_date,
                modifiedDate=db_twin.modified_date
            )

    def create_catalog_part_twin_share(self, global_id: UUID, business_partner_name: str) -> TwinRead:
        # Step 1: Retrieve the twin entity according to the global_id
        # (if not there => raise error)
        # (as an alternative we could also call create_catalog_part_twin() here to create a twin accordingly;
        #  remark: this will not return the primary key of the twin entity; maybe we need to move the logic
        #  to an internal helper function called by both this function and create_catalog_part_twin())

        # Step 2: Retrieve the catalog part entity according to the id of the twin entity
        # (if not there => raise error)

        # Step 3: Retrieve the business partner entity according to the business_partner_name
        # (if not there => raise error)

        # Step 4: Retrieve the data exchange agreement entity for the business partner (with name 'default')
        # (the 'default' agreement will later be replaced with an explicit mechanism)
        # (if not there => raise error)

        # Step 5: Check if there is already a twin exchange entity for the twin and data exchange agreement
        # (if there => we can skip the operation from here on => nothing to do)

        # Step 6: Find the partner catalog part entity for the given catalog part and business partner
        # (if there => fine)
        # (if not there => we normally now would need a customer part ID - either we take it as optional arg
        #  and raise now an error when not there or we create an artificial one; but both need to be reworked
        #  in a later release; finally create the partner catalog part entity)

        # Step 7: Create the twin exchange entity for the twin and data exchange agreement

        # Step 8: Create the shell descriptor in the DTR via the industry core SDK
        # Step 8a: if twin was existing before => add access to the twin for the new business partner
        # (this inculudes: register all specified specific asset IDs visible for partners - e.g. customer part ID - not sure about
        #  manufacturer)
        pass

    def create_twin_aspect(self, twin_aspect_create: TwinAspectCreate) -> TwinAspectRead:
        """
        Create a new twin aspect for a give twin.
        """
        # Step 1: Retrieve the twin entity according to the global_id
        # (if not there => raise error)

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