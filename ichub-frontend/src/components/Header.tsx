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

import { MainNavigation, Button } from '@catena-x/portal-shared-components';

const Header = () => {
  return (
    <MainNavigation
      items={[
        {
          href: '/',
          title: 'Link 1',
        },
        {
          href: '/',
          title: 'Link 2',
        },
        {
          href: '/',
          title: 'Link 3',
        },
        {
          href: '/',
          title: 'Link 4',
        },
      ]}
    >
      <a href="/">
        <img
          src="@/assets/IndustryCoreHubLogo.png"
          alt="Logo"
          style={{
            display: 'inline-block',
            height: '40px',
            width: '170px',
          }}
        />
      </a>
      <div>
        <Button color="secondary" size="small" variant="contained"
          sx={{
            backgroundColor: 'white',
            marginRight: '16px',
          }}
        >
          Help
        </Button>
      </div>
    </MainNavigation>
  );
};

export default Header;
