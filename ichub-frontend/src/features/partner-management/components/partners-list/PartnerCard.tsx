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

import Launch from "@mui/icons-material/Launch";
import { Box, Typography, useTheme, Button } from "@mui/material";

export interface AppContent {
  bpnl?: string;
  name?: string;
}

export interface CardDecisionProps {
  items: AppContent[];
  onClick: (e: string) => void;
}

export const PartnerCard = ({
  items,
  onClick,
}: CardDecisionProps) => {
  const theme = useTheme();

  return (
    <Box
      className="product-cards"
      sx={{
        display: "flex",
        msFlexWrap: "wrap",
        flexWrap: "wrap",
        justifyContent: "center",
      }}
    >
      {items.map((item) => {
        const bpnl = item.bpnl ?? "";
        const name = item.name ?? "";
        return (
          <Box
            key={bpnl}
            sx={{
              paddingRight: "10px",
              paddingLeft: "10px",
              width: "280px",
              minWidth: "280px",
              marginBottom: "20px",
              borderRadius: "5px",
              color: "white",
            }}
          >
            <Box
              className="product-card"
              sx={{
                borderRadius: "8px",
                display: "flex",
                flexDirection: "column",
                width: "auto",
                height: "150px",
                justifyContent: "space-between",
                color: "white",
                cursor: "pointer",
                ":hover": {
                  boxShadow: theme.shadows["20"],
                },
              }}
              onClick={() => {
                onClick(bpnl);
              }}
            >
              <Box
                sx={{
                  padding: "10px 25px",
                }}
              >
                <Typography
                  variant="h5"
                  sx={{
                    WebkitLineClamp: 2,
                    display: "WebkitBox",
                    WebkitBoxOrient: "vertical",
                    overflow: "hidden",
                    fontWeight: "bold",
                    fontSize: "18px",
                    color: "white",
                  }}
                >
                  {name}
                </Typography>
                <br></br>
                <Typography
                  variant="label2"
                  sx={{
                    color: "white",
                    height: "48px",
                  }}
                >
                  {item.bpnl}
                </Typography>
              </Box>
              <Box sx={{ width: "100%" }}>
                <Button
                  variant="contained"
                  size="small"
                  sx={{
                    borderRadius: "8px",
                    borderTopLeftRadius: "0",
                    borderTopRightRadius: "0",
                    background: "rgba(35, 35, 38, 0.76)",
                    width: "100%",
                    ":hover": {
                      background: "linear-gradient(180deg, rgba(1,32,96,0.8323704481792717) 0%, rgba(5,107,153,0.5690651260504201) 100%)"
                    }
                  }}
                  endIcon={<Launch sx={{ color: "white" }} />}
                >
                  View
                </Button>
              </Box>
            </Box>
          </Box>
        );
      })}
    </Box>
  );
};
