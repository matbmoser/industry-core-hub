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

from sqlmodel import SQLModel, Session, select
from typing import TypeVar, Type, List, Optional, Generic

from models.metadata_database.models import BusinessPartner, CatalogPart, DataExchangeAgreement, LegalEntity, PartnerCatalogPart

ModelType = TypeVar("ModelType", bound=SQLModel)

class BaseRepository(Generic[ModelType]):
    def __init__(self, session: Session):
        self._session = session

    def __init_subclass__(cls) -> None:
        # Fetch the model type from the first argument of the generic class

        # pylint: disable=no-member
        cls._type = cls.__orig_bases__[0].__args__[0]  # type: ignore

    @classmethod
    def get_type(cls) -> Type[ModelType]:
        return cls._type  # type: ignore

    def create(self, obj_in: ModelType) -> ModelType:
        self._session.add(obj_in)
        return obj_in
    
    def find_by_id(self, obj_id: int) -> Optional[ModelType]:
        stmt = select(self.get_type()).where(
            self.get_type().id == obj_id)  # type: ignore
        return self._session.scalars(stmt).first()

    def find_all(self, offset: Optional[int] = None, limit: Optional[int] = 100) -> List[ModelType]:
        stmt = select(self.get_type())  # select(Author)
        if offset is not None:
            stmt = stmt.offset(offset)

        if limit is not None:
            stmt = stmt.limit(limit)

        result = self._session.scalars(stmt).unique()
        return list(result)

    def update(self, id: int, obj_in: dict) -> Optional[ModelType]:
        '''
        TODO
        '''
        pass

    def commit(self) -> None:
        self._session.commit()

    def add(self, obj: ModelType, *, commit: bool = False) -> ModelType:
        self._session.add(obj)

        if commit:
            self._session.commit()
            self._session.refresh(obj)
        return obj
    
    def delete(self, obj_id: int, *, commit: bool = False) -> None:
        obj = self._session.get(self.get_type(), obj_id)
        if obj is None:
            err_msg = f'Object not found with id {obj_id}'
            raise ValueError(err_msg)
        self._session.delete(obj)
        if commit:
            self._session.commit()

class BusinessPartnerRepository(BaseRepository[BusinessPartner]):

    def get_by_name(self, name: str) -> Optional[BusinessPartner]:
        stmt = select(BusinessPartner).where(
            BusinessPartner.name == name)  # type: ignore
        return self._session.scalars(stmt).first()

    def get_by_bpnl(self, bpnl: str) -> Optional[BusinessPartner]:
        stmt = select(BusinessPartner).where(
            BusinessPartner.bpnl == bpnl)  # type: ignore
        return self._session.scalars(stmt).first()

class CatalogPartRepository(BaseRepository[CatalogPart]):

    def get_by_legal_entity_id_manufacturer_part_id(self, legal_entity_id: int, manufacturer_part_id: str) -> Optional[CatalogPart]:
        stmt = select(CatalogPart).where(
            CatalogPart.legal_entity_id == legal_entity_id).where(
            CatalogPart.manufacturer_part_id == manufacturer_part_id)
        return self._session.scalars(stmt).first()

    def find_by_manufacturer_id_manufacturer_part_id(self, manufacturer_id: Optional[str], manufacturer_part_id: Optional[str], join_partner_catalog_parts : bool = False) -> List[CatalogPart]:
        stmt = select(CatalogPart).distinct()

        if manufacturer_id:
            stmt = stmt.join(LegalEntity, LegalEntity.id == CatalogPart.legal_entity_id).where(LegalEntity.bpnl == manufacturer_id)

        if manufacturer_part_id:
            stmt = stmt.where(CatalogPart.manufacturer_part_id == manufacturer_part_id)

        if join_partner_catalog_parts:
            subquery = select(PartnerCatalogPart).join(BusinessPartner, BusinessPartner.id == PartnerCatalogPart.business_partner_id).where(PartnerCatalogPart.catalog_part_id == CatalogPart.id).subquery()
            stmt = stmt.join(subquery, subquery.c.catalog_part_id == CatalogPart.id)

        return self._session.exec(stmt).all()

class DataExchangeAgreementRepository(BaseRepository[DataExchangeAgreement]):
    pass

class LegalEntityRepository(BaseRepository[LegalEntity]):

    def get_by_bpnl(self, bpnl: str) -> Optional[LegalEntity]:
        stmt = select(LegalEntity).where(
            LegalEntity.bpnl == bpnl)  # type: ignore
        return self._session.scalars(stmt).first()

class PartnerCatalogPartRepository(BaseRepository[PartnerCatalogPart]):
    pass

