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

import { useState, useEffect, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import sharedPartners from "../tests/payloads/shared-partners.json";
import { PartnerInstance } from "../types/partner";
import TablePagination from '@mui/material/TablePagination';
import { Typography, Grid2, Button } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import { PartnerCard } from "../features/partner-management/components/partners-list/PartnerCard";

const PartnersList = () => {
  const [partnerList, setPartnerList] = useState<PartnerInstance[]>([]);
  const [initialPartnerList, setInitialPartnerList] = useState<PartnerInstance[]>([]);
  const [page, setPage] = useState(0);
  const rowsPerPage = 10;
  const navigate = useNavigate();

  const handleChangePage = (
    _event: React.MouseEvent<HTMLButtonElement> | null,
    newPage: number,
  ) => {
    setPage(newPage);
  };

  useEffect(() => {
    // Define the async function inside useEffect
    const fetchData = async () => {
      try {
        const mappedPartnerList = sharedPartners.map((partner) => ({
          ...partner
        }));
        setPartnerList(mappedPartnerList);
        setInitialPartnerList(mappedPartnerList);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();  // Call the async function
  }, []);

  const handleButtonClick = (partnerBPNL: string) => {
    console.log('Button clicked for partner:', partnerBPNL);
    // For now we will just log the partnerBPNL
    //navigate(`/partner/${partnerBPNL}`);  // Navigate to the details page
  };

  const visibleRows = useMemo(
    () => {
      return [...partnerList].slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
    },
    [page, rowsPerPage, partnerList],
  );

  return (
    <Grid2 className="product-catalog" container spacing={1} direction="row">
      <Grid2 className="title flex flex-content-center">
        <Typography className="text">
          Partners View
        </Typography>
      </Grid2>

      <Grid2 size={12} container justifyContent="flex-end" marginRight={6} marginBottom={2}>
        <Button className="add-partner-button" variant="outlined" size="small" onClick={()=>{}} startIcon={<AddIcon />} >New</Button>
      </Grid2>

      <Grid2 className="flex flex-content-center" size={12}>
        <PartnerCard
          onClick={handleButtonClick}
          items={visibleRows.map((partner) => ({
            bpnl: partner.bpnl,
            name: partner.name,
          }))}
        />
      </Grid2>

      <Grid2 size={12} className="flex flex-content-center">
        <TablePagination
          rowsPerPageOptions={[rowsPerPage]}
          component="div"
          count={initialPartnerList.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          className="product-list-pagination"
        />
      </Grid2>
    </Grid2>
  );
};

export default PartnersList;
