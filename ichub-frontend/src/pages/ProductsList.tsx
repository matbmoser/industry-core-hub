
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
import carPartsData from "../tests/payloads/sample-data.json";
import { ProductCard } from "../components/general/ProductCard";
import { PartInstance } from "../types/product";
import  Grid2  from "@mui/material/Grid2";
import TablePagination from '@mui/material/TablePagination';
import TopSearch from "../components/general/Search";


const ProductsList = () => {
  const [carParts, setCarParts] = useState<PartInstance[]>([]);
  const [initialCarParts, setInitialCarParts] = useState<PartInstance[]>([]);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);


   const handleChangePage = (
    event: React.MouseEvent<HTMLButtonElement> | null,
    newPage: number,
  ) => {
    setPage(newPage);
  };
  const navigate = useNavigate();
  useEffect(() => {
    // Define the async function inside useEffect
    const fetchData = async () => {
      try {
        const data = await carPartsData;  // Resolve the promise
        setCarParts(data);
        setInitialCarParts(data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
  
    fetchData();  // Call the async function
  }, []);

  const handleButtonClick = (part: PartInstance) => {
    navigate(`/product/${part.uuid}`);  // Navigate to the details page
  };

  const visibleRows = useMemo(
    () =>
      {
        return [...carParts].slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
      },
    [page, rowsPerPage,carParts],
  );

  return (
    <Grid2 className="product-catalog" container spacing={1} direction="row">
      
      <Grid2 size={{ xs: 5}} display="flex" justifyContent="center" >
        <span className="text">
          Catalog Parts
        </span>
      </Grid2>
     <Grid2 size={{ xs: 7}} display="flex" justifyContent="end">
        <TopSearch></TopSearch>
      </Grid2> 
     
      <Grid2 className="flex flex-content-center">
        <ProductCard
          onClick={(itemId: any) => handleButtonClick(itemId)}
          items={visibleRows.map((part) => ({
            uuid: part.uuid,
            name: part.name,
            class: part.class,
            status: part.status,
          }))}
        />
      </Grid2>
      <Grid2 size={{ xs: 12}} display="flex" justifyContent="center" className="pagination-text">
      <TablePagination
          rowsPerPageOptions={[10]}
          component="div"
          count={initialCarParts.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
        />
      </Grid2>
    </Grid2>
  );
};

export default ProductsList;
