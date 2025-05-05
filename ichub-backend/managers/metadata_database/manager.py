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
# WITHOUT WARRANTIES OR CONDITIONS,
# either express or implied. See the
# License for the specific language govern in permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0
#################################################################################

from threading import Lock

from sqlmodel import create_engine, Session

class RepositoryManager:
    """Repository manager for managing repositories and handling the session."""

    def __init__(self, session: Session):
        self._session = session
        self._business_partner_repository = None
        self._catalog_part_repository = None
        self._data_exchange_agreement_repository = None
        self._enablement_service_stack_repository = None
        self._legal_entity_repository = None
        self._partner_catalog_part_repository = None
        self._twin_repository = None
        self._twin_exchange_repository = None
        self._twin_registration_repository = None

    # Context Manager Methods
    def __enter__(self):
        """Enter the context, ensuring the session is active."""
        if not self._session.is_active:
            self._session.begin()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the context, committing or rolling back the session."""
        if exc_type is None:
            self._session.commit()
        else:
            self._session.rollback()
        self._session.close()

    # Manual Session Control
    def commit(self):
        """Manually commit the session."""
        self._session.commit()

    def rollback(self):
        """Manually roll back the session."""
        self._session.rollback()

    def close(self):
        """Manually close the session."""
        self._session.close()

    def refresh(self, obj):
        """Refresh the state of an instance from the database."""
        self._session.refresh(obj)

    # Lazy Initialization of Repositories
    @property
    def business_partner_repository(self):
        """Lazy initialization of the business partner repository."""
        if self._business_partner_repository is None:
            from managers.metadata_database.repositories import BusinessPartnerRepository
            self._business_partner_repository = BusinessPartnerRepository(self._session)
        return self._business_partner_repository

    @property
    def catalog_part_repository(self):
        """Lazy initialization of the catalog part repository."""
        if self._catalog_part_repository is None:
            from managers.metadata_database.repositories import CatalogPartRepository
            self._catalog_part_repository = CatalogPartRepository(self._session)
        return self._catalog_part_repository

    @property
    def data_exchange_agreement_repository(self):
        """Lazy initialization of the data exchange agreement repository."""
        if self._data_exchange_agreement_repository is None:
            from managers.metadata_database.repositories import DataExchangeAgreementRepository
            self._data_exchange_agreement_repository = DataExchangeAgreementRepository(self._session)
        return self._data_exchange_agreement_repository

    @property
    def enablement_service_stack_repository(self):
        """Lazy initialization of the enablement service stack repository."""
        if self._enablement_service_stack_repository is None:
            from managers.metadata_database.repositories import EnablementServiceStackRepository
            self._enablement_service_stack_repository = EnablementServiceStackRepository(self._session)
        return self._enablement_service_stack_repository

    @property
    def legal_entity_repository(self):
        """Lazy initialization of the legal entity repository."""
        if self._legal_entity_repository is None:
            from managers.metadata_database.repositories import LegalEntityRepository
            self._legal_entity_repository = LegalEntityRepository(self._session)
        return self._legal_entity_repository

    @property
    def partner_catalog_part_repository(self):
        """Lazy initialization of the partner catalog part repository."""
        if self._partner_catalog_part_repository is None:
            from managers.metadata_database.repositories import PartnerCatalogPartRepository
            self._partner_catalog_part_repository = PartnerCatalogPartRepository(self._session)
        return self._partner_catalog_part_repository
    
    @property
    def twin_repository(self):
        """Lazy initialization of the twin repository."""
        if self._twin_repository is None:
            from managers.metadata_database.repositories import TwinRepository
            self._twin_repository = TwinRepository(self._session)
        return self._twin_repository

    @property
    def twin_exchange_repository(self):
        """Lazy initialization of the twin exchange repository."""
        if self._twin_exchange_repository is None:
            from managers.metadata_database.repositories import TwinExchangeRepository
            self._twin_exchange_repository = TwinExchangeRepository(self._session)
        return self._twin_exchange_repository

    @property
    def twin_registration_repository(self):
        """Lazy initialization of the twin registration repository."""
        if self._twin_registration_repository is None:
            from managers.metadata_database.repositories import TwinRegistrationRepository
            self._twin_registration_repository = TwinRegistrationRepository(self._session)
        return self._twin_registration_repository

class RepositoryManagerFactory:
    """Factory class for creating repository managers with singleton behavior."""

    _engine_instance = None
    _repository_manager_instance = None
    _lock: Lock = Lock()

    @staticmethod
    def create(db_url: str = "postgresql://username:password@localhost/dbname") -> RepositoryManager:
        """Create or return the singleton instance of RepositoryManager."""
        if RepositoryManagerFactory._repository_manager_instance is None:
            with RepositoryManagerFactory._lock:
                if RepositoryManagerFactory._repository_manager_instance is None:
                    # Create a SQLModel engine for PostgreSQL if not already created
                    if RepositoryManagerFactory._engine_instance is None:
                        RepositoryManagerFactory._engine_instance = create_engine(db_url)

                    # Create the singleton instance of RepositoryManager
                    session = Session(RepositoryManagerFactory._engine_instance)
                    RepositoryManagerFactory._repository_manager_instance = RepositoryManager(session)

        return RepositoryManagerFactory._repository_manager_instance