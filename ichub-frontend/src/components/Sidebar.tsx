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

import { Menu } from '@catena-x/portal-shared-components';

const Sidebar = () => {
  return (
    <Menu
      items={[
        {
          children: [
            {
              href: '/',
              title: 'Submenu Item 1'
            },
            {
              href: '/',
              title: 'Submenu Item 2'
            },
            {
              disable: true,
              hint: 'coming soon',
              href: '/',
              title: 'Submenu Item 3'
            }
          ],
          href: '/',
          title: 'Menu Item 1'
        },
        {
          href: '/',
          title: 'Menu Item 2'
        },
        {
          href: '/',
          title: 'Menu Item 3'
        }
      ]}
    />
  )
}

export default Sidebar