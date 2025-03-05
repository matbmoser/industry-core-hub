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

import React from "react";
import { useParams } from "react-router-dom";
import carPartsData from "../data/sample-data.json";
import { DropdownMenu, StatusTag, Button, Icon, Typography, PageNotifications } from '@catena-x/portal-shared-components';
import { PRODUCT_STATUS, PRODUCT_OPTIONS } from "../types/common";


const ProductsDetails = () => {
  const { id } = useParams<{ id: string }>();
  const part = carPartsData.find((part) => part.uuid === id);
  const [dialogOpen, setDialogOpen] = React.useState(false);
  const [notification, setNotification] = React.useState<{ open: boolean; severity: "success" | "error"; title: string } | null>(null);

  if (!part) {
    return <div>Product not found</div>;
  }

  const handleOpenDialog = () => {
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(part.uuid)
      .then(() => {
        setNotification({
          open: true,
          severity: "success",
          title: "PartInstanceID copied to clipboard",
        });
        setTimeout(() => setNotification(null), 15500); // Cierra la notificación después de 3 segundos
      })
      .catch((error) => {
        setNotification({
          open: true,
          severity: "error",
          title: "Failed to copy PartInstanceID",
        });
        setTimeout(() => setNotification(null), 15500); // Cierra la notificación después de 3 segundos
        console.error("Failed to copy text: ", error);
      });
  };

  const handleDownload = () => {
    const fileName = part.Name.toLowerCase().replace(/\s+/g, "-") + ".txt";
    const blob = new Blob([part.uuid], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: part.Name,
          text: `Check out this part: ${part.Name} (UUID: ${part.uuid})`,
          url: window.location.href
        });
      } catch (error) {
        console.error("Error sharing:", error);
      }
    } else {
      console.log("Web Share API not supported.");
    }
  };


  const getStatusTag = (status: string) => {
    switch (status.toLowerCase()) {
      case PRODUCT_STATUS.REGISTERED:
        return <StatusTag color="confirmed" label="Registered" variant="filled" />;
      case PRODUCT_STATUS.DRAFT:
        return <StatusTag color="declined" label="Draft" variant="filled" />;
      case PRODUCT_STATUS.PENDING:
        return <StatusTag color="pending" label="Pending" variant="filled" />;
      default:
        return null;
    }
  };

  return (
    <div className="productDetail">
      {notification && (
        <div style={{ maxWidth: '300px', marginLeft: 'auto' }}>
          <PageNotifications open severity="success" showIcon title="Copy successful" />
        </div>
      )}
      <div className="flex flex-content-between mx-3">
        {getStatusTag(part.Status)}
        <Button size="small"
          onClick={() => console.log("DCM v2.0 button")}
          style={{
            backgroundColor: "purple",
            height: "32px",
            boxSizing: "border-box",
            borderRadius: "6px",
            fontSize: "0.8125rem"
          }}>
          <Icon fontSize="16" iconName="Edit" />
          Edit
        </Button>
      </div>
      <div className="grid-70-30" style={{ marginBottom: "7%" }}>
        <div>
          <div className="my-5 flex flex-content-between px-3">
            <div className="title-subtitle">
              <Typography variant="h2">{part.Name}</Typography>
              <Typography variant="caption1">{part.Category}</Typography>
            </div>
            <DropdownMenu
              buttonSx={{
                'padding': '10px 10px',
                'border': '1px solid #b4b4b4!important',
                'font-size': '14px',
              }}
              buttonText="Share"
            >
              <div className="flex flex-column">
                <Button color="secondary" size="small" onClick={handleCopy} className="share-dropdown-btn">
                  <Icon fontSize="16" iconName="ContentCopy" />
                  {PRODUCT_OPTIONS.COPY}
                </Button>
                <Button color="secondary" size="small" onClick={handleDownload} className="share-dropdown-btn">
                  <Icon fontSize="16" iconName="FileDownload" />
                  {PRODUCT_OPTIONS.DOWNLOAD}
                </Button>
                <Button color="secondary" size="small" onClick={handleShare} className="share-dropdown-btn">
                  <Icon fontSize="16" iconName="IosShare" />
                  {PRODUCT_OPTIONS.SHARE}
                </Button>
              </div>
            </DropdownMenu>
          </div>

          <div>
            <div className="flex mb-1">
              <Typography variant="label2" style={{ marginRight: "5px" }}>🔢 Part Instance ID:</Typography>
              <Typography variant="body2">{part.PartInstanceID}</Typography>
            </div>
            <div className="flex mb-1">
              <Typography variant="label2" style={{ marginRight: "5px" }}>🏭 Manufacturer:</Typography>
              <Typography variant="body2">{part.Manufacturer}</Typography>
            </div>
            <div className="flex mb-1">
              <Typography variant="label2" style={{ marginRight: "5px" }}>📌 Status:</Typography>
              <Typography variant="body2">{part.Status}</Typography>
            </div>
            <div className="flex mb-1">
              <Typography variant="label2" style={{ marginRight: "5px" }}>🔩 Material:</Typography>
              <Typography variant="body2">{part.Material}</Typography>
            </div>
            <div className="flex mb-1">
              <Typography variant="label2" style={{ marginRight: "5px" }}>📂 Category:</Typography>
              <Typography variant="body2">{part.Category}</Typography>
            </div>
            <div className="flex mb-1">
              <Typography variant="label2" style={{ marginRight: "5px" }}>⚖️ Weight:</Typography>
              <Typography variant="body2">{part.WeightKg} kg</Typography>
            </div>
            <div className="flex mb-1">
              <Typography variant="label2" style={{ marginRight: "5px" }}>📊 Single Level Bom:</Typography>
              <Typography variant="body2">{part.SingleLevelBom} kg</Typography>
            </div>
            <div className="flex mb-1">
              <Typography variant="label2" style={{ marginRight: "5px" }}>📝 Description:</Typography>
              <Typography variant="body2">{part.Description} kg</Typography>
            </div>
          </div>
        </div>
        <div className="my-auto">
          <img src={part.Image} alt={part.Name} className="img-fluid my-auto" />
          <div className="mt-3">
            <ul>
              <li className="flex">
                <Icon fontSize="16" iconName="Polyline" className="my-auto mr-1" />
                <Typography variant="label2" style={{ marginRight: "5px" }}>Relationship 1:</Typography>
                <Typography variant="body2">PI-702</Typography>
              </li>
              <li className="flex">
                <Icon fontSize="16" iconName="Polyline" className="my-auto mr-1" />
                <Typography variant="label2" style={{ marginRight: "5px" }}>Relationship 2:</Typography>
                <Typography variant="body2">PI-244</Typography>
              </li>
              <li className="flex">
                <Icon fontSize="16" iconName="Polyline" className="my-auto mr-1" />
                <Typography variant="label2" style={{ marginRight: "5px" }}>Relationship 3:</Typography>
                <Typography variant="body2">PI-089</Typography>
              </li>
              <li className="flex">
                <Icon fontSize="16" iconName="Polyline" className="my-auto mr-1" />
                <Typography variant="label2" style={{ marginRight: "5px" }}>Relationship 4:</Typography>
                <Typography variant="body2">PI-011</Typography>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <div className="flex m-5">
        <Button color="success" size="large" onClick={() => console.log("Add button")} fullWidth={true} style={{ padding: "5px" }}>
          <Icon fontSize="18" iconName="Add" />
        </Button>
      </div>

      <div className="flex m-5 flex-content-between flex-gap-5">
        <Button color="primary" size="large" onClick={() => console.log("PCF v3.0 button")} fullWidth={true} style={{ padding: "10px" }}>
          <Icon fontSize="16" iconName="Add" />
          PCF v3.0
        </Button>
        <Button color="primary" size="large" onClick={() => console.log("DPP v2.0 button")} fullWidth={true} style={{ padding: "10px" }}>
          <Icon fontSize="16" iconName="Add" />
          DPP v2.0
        </Button>
        <Button color="primary" size="large" onClick={handleOpenDialog} fullWidth={true} style={{ padding: "10px" }}>
          <Icon fontSize="16" iconName="Add" />
          DCM v2.0
        </Button>
      </div>
      <div className="flex m-5">
        <Button color="error" size="large" onClick={() => console.log("Transmission Passport v5.0")} fullWidth={true} style={{ padding: "10px" }}>
          <Icon fontSize="16" iconName="Add" />
          Transmission Passport v5.0
        </Button>
      </div>
    </div>
  );
}

export default ProductsDetails