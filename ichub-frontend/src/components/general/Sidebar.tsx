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

import { useState, JSX } from "react";
import sidebarElements from '../../tests/payloads/sidebar-elements.json'

import { Box } from "@mui/material";

import { Storefront as StorefrontIcon, Category as CategoryIcon, People as PeopleIcon, Assignment as AssignmentIcon } from '@mui/icons-material';

const iconMap: { [key: string]: JSX.Element } = {
  Storefront: <StorefrontIcon />, 
  Category: <CategoryIcon />, 
  Shared: <PeopleIcon />, 
  Status: <AssignmentIcon />
};

const Sidebar = () => {
  const [activeIndex, setActiveIndex] = useState(0);

  return (
    <Box className="sidebarContainer">
      {/* Barra de Iconos */}
      <Box className="iconBar">
        {sidebarElements.map((item, index) => (
          <button
            key={index}
            className={`iconButton ${index === activeIndex ? "active" : ""}`}
            onClick={() => setActiveIndex(index)}
          >
            {iconMap[item.icon] || <StorefrontIcon />}
          </button>
        ))}
      </Box>

      {/* Contenido del Sidebar */}
      <Box className="sidebarContent">
        <h2>{sidebarElements[activeIndex].title}</h2>
        <ul>
          {sidebarElements[activeIndex].subitems.map((subitem, idx) => (
            <li key={idx}>
              <a href={subitem.link}>{subitem.name}</a>
            </li>
          ))}
        </ul>
      </Box>
    </Box>
  );
};

export default Sidebar