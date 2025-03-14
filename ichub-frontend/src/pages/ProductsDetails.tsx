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
import carPartsData from "../tests/payloads/sample-data.json";
import instanceData from "../tests/payloads/instance-data.json";
import { DropdownMenu, StatusTag, Button, Icon, Typography, PageNotifications, Table } from '@catena-x/portal-shared-components';
import { PRODUCT_STATUS, PRODUCT_OPTIONS } from "../types/common";
import JsonViewerDialog from "../components/general/JsonViewerDialog";
import { Box, Grid2 } from '@mui/material';
import InstanceProductsTable from "../components/product-detail/InstanceProductsTable";

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
    const fileName = part.name.toLowerCase().replace(/\s+/g, "-") + ".txt";
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
          title: part.name,
          text: `Check out this part: ${part.name} (UUID: ${part.uuid})`,
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
        return <StatusTag color="confirmed" label="Registered" variant="outlined" />;
      case PRODUCT_STATUS.DRAFT:
        return <StatusTag color="info" label="Draft" variant="outline" />;
      case PRODUCT_STATUS.SHARED:
        return <StatusTag color="warning" label="Shared" variant="filled" />;
      default:
        return null;
    }
  };

  return (
    <>      
      {notification && (
        <Grid2 size={{xs: 12}}>
          <PageNotifications open severity={notification.severity} showIcon title={notification.title} />
        </Grid2>
      )}
      
      <Grid2 container direction="column" className="productDetail">
        <Grid2 container spacing={2} className="mb-5" justifyContent={{ md: "space-between", sm: "center" }} alignItems="center" direction={{ sm: "column", md: "row" }}>
          <Grid2 size={{md: 3, sm: 12}} display="flex" justifyContent="center">
            {getStatusTag(part.status)}
          </Grid2>
          <Grid2 size={{md: 3, sm: 12}} display="flex" justifyContent="center">
            <Button size="small" onClick={() => console.log("DCM v2.0 button")} className="update-button" endIcon={<Icon fontSize="16" iconName="Edit" />}>            
                <span className="update-button-content">UPDATE</span>            
            </Button>
          </Grid2>
          <Grid2 size={{md: 3, sm: 12}} display="flex" justifyContent="center">
            <DropdownMenu
              buttonSx={{
                'padding': '10px 10px',
                'border': '1px solid #b4b4b4!important',
                'font-size': '14px',
              }}
              buttonText="Share"
              startIcon={<Icon fontSize="16" iconName="IosShare" />}
            >
              <Grid2 container direction="column">
                <Button className="dropdown-button share-dropdown-btn" color="secondary" size="small" onClick={handleCopy} startIcon={<Icon fontSize="16" iconName="ContentCopy" />}>
                  <span className="dropdown-button-content">{PRODUCT_OPTIONS.COPY}</span>
                </Button>
                <Button className="dropdown-button share-dropdown-btn" color="secondary" size="small" onClick={handleDownload} startIcon={<Icon fontSize="16" iconName="FileDownload" />}>
                  <span className="dropdown-button-content">{PRODUCT_OPTIONS.DOWNLOAD}</span>
                </Button>
                <Button className="dropdown-button share-dropdown-btn" color="secondary" size="small" onClick={handleShare} startIcon={<Icon fontSize="16" iconName="IosShare" />}>
                  <span className="dropdown-button-content">{PRODUCT_OPTIONS.SHARE}</span>
                </Button>
              </Grid2>
            </DropdownMenu>
          </Grid2>
        </Grid2>

        <Grid2 container justifyContent="space-between" className="mb-5">
          <Grid2 size={{lg: 4, md: 12}}>
            <Grid2 className="title-subtitle">
                <Typography variant="h2">{part.name}</Typography>
                <Typography variant="caption1">{part.class}</Typography>
            </Grid2>

            <Grid2 className="ml-3 mb-2 product-card">
              <Box>
                <Typography variant="label3">Manufacturer</Typography>
                <Typography variant="body1">{part.manufacturer}</Typography>
              </Box>
              <Box>
                <Typography variant="label3">Manufacturer Part Id</Typography>
                <Typography variant="body1">{part.manufacturerPartId}</Typography>
              </Box>
              <Box>
                <Typography variant="label4">Description</Typography>
                <Typography variant="body2">{part.description}</Typography>
              </Box>
              <Grid2 container>
                <Grid2 size={{md:6, xs:12}}>
                  <Typography variant="label4">Created</Typography>
                  <Typography variant="body2">{part.created}</Typography>
                </Grid2>
                <Grid2 size={{md:6, xs:12}}>
                  <Typography variant="label4">Updated</Typography>
                  <Typography variant="body2">{part.created}</Typography>
                </Grid2>
              </Grid2>
            </Grid2>
          </Grid2>
          <Grid2 size={{lg: 4, md: 12}} alignContent="right" alignItems="right">
            <img src={part.image} alt={part.name} className="product-image img-fluid my-auto" />
            <Box>
              <Typography variant="label4">{part.uuid}</Typography>
            </Box>
            <h2 className="mt-4">Shared With:</h2>
              <ul className="mt-3">
                <li className="flex">
                  <Icon fontSize="16" iconName="Polyline" className="my-auto mr-1" />
                  <Typography variant="label2" style={{ marginRight: "5px" }}>Volkswagen AG -</Typography>
                  <Typography variant="body2">BPNL42621500AS61</Typography>
                </li>
                <li className="flex">
                  <Icon fontSize="16" iconName="Polyline" className="my-auto mr-1" />
                  <Typography variant="label2" style={{ marginRight: "5px" }}>BMW Racing Gmbh -</Typography>
                  <Typography variant="body2">BPNL3A4T8A5621S3</Typography>
                </li>
                <li className="flex">
                  <Icon fontSize="16" iconName="Polyline" className="my-auto mr-1" />
                  <Typography variant="label2" style={{ marginRight: "5px" }}>John the Recycler KG - </Typography>
                  <Typography variant="body2">BPNL5ASD5428800A</Typography>
                </li>
                <li className="flex">
                  <Icon fontSize="16" iconName="Launch" className="my-auto mr-1" />
                  <a href="">512 more</a>
                </li>
              </ul>
          </Grid2>
        </Grid2>

        <Grid2 container spacing={2} direction="column" className="add-on-buttons">
          <Grid2 size={{ sm: 12 }}>
            <Button className="submodel-button" variant="outlined" color="primary" size="large" onClick={handleOpenDialog} fullWidth={true}>
              <span className="submodel-button-content">DIGITAL PRODUCT PASSPORT v5.0.0</span>
              <Icon fontSize="16" iconName="OpenInNew" />
            </Button>
          </Grid2>

        <Grid2 container spacing={2} justifyContent="center">
          <Grid2 size={{ lg: 4, md: 12, sm: 12 }}>
            <Button className="submodel-button" variant="outlined" color="primary" size="large" onClick={() => console.log("PCF v3.0 button")} fullWidth={true}>
              <span className="submodel-button-content">PCF v3.0.0</span>
              <Icon fontSize="16" iconName="OpenInNew" />
            </Button>
          </Grid2>
          <Grid2 size={{ lg: 4, md: 12, sm: 12 }}>
            <Button className="submodel-button" variant="outlined" color="primary" size="large" onClick={() => console.log("DPP v2.0 button")} fullWidth={true}>
              <span className="submodel-button-content">TRANSMISSION PASS v2.0.0</span>
              <Icon fontSize="16" iconName="OpenInNew" />
            </Button>
          </Grid2>
          <Grid2 size={{ lg: 4, md: 12, sm: 12 }}>
            <Button className="submodel-button" variant="outlined"color="primary" size="large" fullWidth={true}>
              <span className="submodel-button-content">DCM v2.0.0</span>
              <Icon fontSize="16" iconName="OpenInNew" />
            </Button>
          </Grid2>
        </Grid2>
        <Grid2 size={{ sm: 12 }}>
          <Button className="submodel-button" color="success" size="small" onClick={() => console.log("Add button")} fullWidth={true} style={{ padding: "5px" }}>
            <Icon fontSize="18" iconName="Add" />
          </Button>
        </Grid2>

        </Grid2>

        <JsonViewerDialog open={dialogOpen} onClose={handleCloseDialog} carJsonData={part}/>
      </Grid2>
      
      <InstanceProductsTable />
    </>
  );
}

export default ProductsDetails