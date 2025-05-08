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

from tractusx_sdk.industry.services import AasService
from tractusx_sdk.industry.models.aas.v3 import (
    Endpoint,
    ShellDescriptor,
    SubModelDescriptor,
    SpecificAssetId,
    Reference,
    ReferenceTypes,
    ReferenceKeyTypes,
    ReferenceKey,
    Result,
    ProtocolInformationSecurityAttributesTypes,
    ProtocolInformation,
    ProtocolInformationSecurityAttributes,
)
from typing import Dict
from uuid import UUID
from urllib import parse

from config.config_manager import ConfigManager
from tools.aspect_id_tools import extract_aspect_id_name_from_urn_camelcase

class DTRManager:
    def __init__(
        self,
        dtr_url: str,
        dtr_lookup_url: str,
        api_path: str,
    ):
        self.dtr_url = dtr_url
        self.dtr_lookup_url = dtr_lookup_url
        self.aas_service = AasService(
            base_url=dtr_url,
            base_lookup_url=dtr_lookup_url,
            api_path=api_path,
        )
        self.edc_controlplane_hostname = ConfigManager.get_config(
            "edc.controlplane.hostname"
        )
        self.edc_controlplane_catalog_path = ConfigManager.get_config(
            "edc.controlplane.catalogPath"
        )
        self.edc_dataplane_hostname = ConfigManager.get_config("edc.dataplane.hostname")
        self.edc_dataplane_public_path = ConfigManager.get_config(
            "edc.dataplane.publicPath"
        )

    def create_shell_descriptor(
        self,
        aas_id: UUID,
        global_id: UUID,
        manufacturer_id: str,
        manufacturer_part_id: str,
        customer_part_ids: Dict[str, str],
        part_category: str,
    ) -> ShellDescriptor:
        """
        Registers a twin in the DTR.
        """
        specific_asset_ids = []
        for customer_part_id, bpn in customer_part_ids.items():
            specific_customer_part_asset_id = SpecificAssetId(
                name="customerPartId",
                value=customer_part_id,
                externalSubjectId=Reference(
                    type=ReferenceTypes.EXTERNAL_REFERENCE,
                    keys=[
                        ReferenceKey(
                            type=ReferenceKeyTypes.GLOBAL_REFERENCE, value=bpn
                        ),
                    ],
                ),
            )  # type: ignore
            specific_asset_ids.append(specific_customer_part_asset_id)

        specific_manufacturer_asset_id = SpecificAssetId(
            name="manufacturerId",
            value=manufacturer_id,
            externalSubjectId=Reference(
                type=ReferenceTypes.EXTERNAL_REFERENCE,
                keys=[
                    ReferenceKey(type=ReferenceKeyTypes.GLOBAL_REFERENCE, value=bpn)
                    for bpn in customer_part_ids.values()
                ],
            ),
        )  # type: ignore
        specific_asset_ids.append(specific_manufacturer_asset_id)

        digital_twin_asset_id = SpecificAssetId(
            name="digitalTwinType",
            value="PartType",
            externalSubjectId=Reference(
                type=ReferenceTypes.EXTERNAL_REFERENCE,
                keys=[
                    ReferenceKey(type=ReferenceKeyTypes.GLOBAL_REFERENCE, value=bpn)
                    for bpn in customer_part_ids.values()
                ],
            ),
        )  # type: ignore
        specific_asset_ids.append(digital_twin_asset_id)

        specific_manufacturer_part_asset_id = SpecificAssetId(
            name="manufacturerPartId",
            value=manufacturer_part_id,
            externalSubjectId=Reference(
                type=ReferenceTypes.EXTERNAL_REFERENCE,
                keys=[
                    ReferenceKey(
                        type=ReferenceKeyTypes.GLOBAL_REFERENCE, value="PUBLIC_READABLE"
                    ),
                ],
            ),
        )  # type: ignore
        specific_asset_ids.append(specific_manufacturer_part_asset_id)

        # ids need to be saved as urn
        shell = ShellDescriptor(
            id=aas_id.urn,
            globalAssetId=global_id.urn,
            specificAssetIds=specific_asset_ids,
        )  # type: ignore

        res = self.aas_service.create_asset_administration_shell_descriptor(shell)
        if isinstance(res, Result):
            raise Exception("Error creating shell descriptor", res)
        return res

    def create_submodel_descriptor(
        self,
        global_id: UUID,
        aas_id: UUID,
        submodel_id: UUID,
        semantic_id: str,
        edc_asset_id: UUID,
    ) -> SubModelDescriptor:
        """
        Creates a submodel descriptor in the DTR.
        """
        aspect_id_name = extract_aspect_id_name_from_urn_camelcase(semantic_id)

        semantic_id_reference = Reference(
            type=ReferenceTypes.EXTERNAL_REFERENCE,
            keys=[
                ReferenceKey(type=ReferenceKeyTypes.GLOBAL_REFERENCE, value=semantic_id)
            ],
        )

        href_url = f"{self.edc_dataplane_hostname}{self.edc_dataplane_public_path}/{semantic_id}/{global_id.urn}/submodel"

        parsed_href_url = parse.urlparse(href_url)
        if not (parsed_href_url.scheme == "https" and parsed_href_url.netloc):
            raise Exception(f"Generated href URL is malformed: {href_url}")

        dsp_endpoint_url = f"{self.edc_controlplane_hostname}{self.edc_controlplane_catalog_path}"
        parsed_dsp_endpoint_url = parse.urlparse(dsp_endpoint_url)
        if not (
            parsed_dsp_endpoint_url.scheme == "https" and parsed_dsp_endpoint_url.netloc
        ):
            raise Exception(
                f"Generated DSP endpoint URL for subprotocolBody is malformed: {dsp_endpoint_url}"
            )

        subprotocol_body_str = f"dspEndpoint={dsp_endpoint_url};id={edc_asset_id.urn}"

        endpoint = Endpoint(
            interface="SUBMODEL-3.0",
            protocolInformation=ProtocolInformation(
                href=href_url,
                endpointProtocol="HTTP",
                endpointProtocolVersion=["1.1"],
                subprotocol="DSP",
                subprotocolBody=subprotocol_body_str,
                subprotocolBodyEncoding="plain",
                securityAttributes=[
                    ProtocolInformationSecurityAttributes(
                        type=ProtocolInformationSecurityAttributesTypes.NONE,
                        key="NONE",
                        value="NONE",
                    )
                ],  # type: ignore
            ),  # type: ignore
        )
        submodel = SubModelDescriptor(
            id=submodel_id.urn,
            idShort=aspect_id_name,
            semanticId=semantic_id_reference,
            endpoints=[endpoint],
        )  # type: ignore

        res = self.aas_service.create_submodel_descriptor(aas_id.urn, submodel)
        if isinstance(res, Result):
            raise Exception("Error creating submodels descriptor", res)
        return res
