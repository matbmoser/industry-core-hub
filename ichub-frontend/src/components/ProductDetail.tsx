/********************************************************************************
 * Eclipse Tractus-X - Industry Core Hub Frontend
 *
 * Copyright (c) 2025 Contributors to the Eclipse Foundation
 *
 * See the NOTICE file(s) distributed with this work for additional
 * information regarding copyright ownership.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Apache License, Version 2.0 which is available at
 * https://www.apache.org/licenses/LICENSE-2.0.
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
 * either express or implied. See the
 * License for the specific language govern in permissions and limitations
 * under the License.
 *
 * SPDX-License-Identifier: Apache-2.0
********************************************************************************/

import { useParams } from "react-router-dom";
import carPartsData from "../data/sample-data.json";
import { DropdownMenu, StatusTag, Button, Icon, Typography } from '@catena-x/portal-shared-components';

interface CarPart {
    uuid: string;
    PartInstanceID: string;
    Name: string;
    Status: string;
    SingleLevelBom: string;
    Manufacturer: string;
    Material: string;
    WeightKg: number;
    Category: string;
    Description: string;
    Image: string;
  }

function ProductDetail() {
  const { id } = useParams<{ id: string }>();
  const part = carPartsData.find((part) => part.uuid === id);

  if (!part) {
    return <div>Product not found</div>;
  }

  return (
    <div>
        <Typography variant="h1" className="rolesAddedHeading">{part.Name}</Typography>
        <StatusTag color="confirmed" label="Registered" variant="filled" />
        <StatusTag color="declined" label="Draft" variant="filled" />
        <StatusTag color="pending" label="Pending" variant="filled" />
        <DropdownMenu buttonText="Share">
            <Button color="secondary" size="small" onClick={() => console.log("Copy unique ID")}>
            <Icon fontSize="16" iconName="ContentCopy" /> 
                Copy unique ID
            </Button>
            <Button color="secondary" size="small" onClick={() => console.log("Download")}>
                <Icon fontSize="16" iconName="FileDownload" /> 
                Download
            </Button>
            <Button color="secondary" size="small" onClick={() => console.log("Share with partner")}>
                <Icon fontSize="16" iconName="IosShare" /> 
            Share with partner
            </Button>
        </DropdownMenu>
        <p><strong>Part Instance ID:</strong> {part.PartInstanceID}</p>
        <p><strong>Manufacturer:</strong> {part.Manufacturer}</p>
        <p><strong>Status:</strong> {part.Status}</p>
        <p><strong>Material:</strong> {part.Material}</p>
        <p><strong>Category:</strong> {part.Category}</p>
        <p><strong>Weight:</strong> {part.WeightKg} kg</p>
        <p><strong>Single Level Bom:</strong> {part.SingleLevelBom} kg</p>
        <p><strong>Description:</strong> {part.Description} kg</p>
        <img src={part.Image} alt={part.Name} />
        
        <Button color="success" size="large" onClick={() => console.log("Add button")}>
                <Icon fontSize="16" iconName="Add" /> 
            Share with partner
        </Button>
    </div>
  );
}

export default ProductDetail;
