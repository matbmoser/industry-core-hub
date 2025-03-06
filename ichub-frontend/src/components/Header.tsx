import { useState } from 'react';
import { MainNavigation, Button, IconButton } from '@catena-x/portal-shared-components';
import PersonIcon from '@mui/icons-material/Person';
import { Menu, MenuItem, Typography, Divider, ListItemIcon } from '@mui/material';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import SettingsIcon from '@mui/icons-material/Settings';
import LogoutIcon from '@mui/icons-material/Logout';

const Header = () => {
  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  return (
    <MainNavigation
      items={[
        { href: '/', title: 'Industry Core Hub' },
      ]}
    >
      <a href="/">
        <img
          src="/eclipse-tractus-x-logo.png"
          alt="Eclipse Tractus-X logo"
          style={{ display: 'inline-block', height: '40px', width: '170px' }}
        />
      </a>
      <div>
        <IconButton aria-label="user-menu" onClick={handleMenuOpen}>
          <PersonIcon />
        </IconButton>
        <Menu
          anchorEl={anchorEl}
          open={open}
          onClose={handleMenuClose}
          className='navbar-user-dropdown'
        >
          {/* Encabezado con nombre y email */}
          <Typography variant="subtitle1" sx={{ padding: '8px 16px 0px 16px', fontWeight: 'bold' }}>
            Mathias Brunkow Moser
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ padding: '0 16px 8px', fontStyle: 'italic' }}>
            CX-Operator
          </Typography>
          <Divider />

          {/* Opciones del menú */}
          <MenuItem onClick={handleMenuClose}>
            <ListItemIcon>
              <AccountCircleIcon fontSize="small" />
            </ListItemIcon>
            Profile
          </MenuItem>
          <MenuItem onClick={handleMenuClose}>
            <ListItemIcon>
              <SettingsIcon fontSize="small" />
            </ListItemIcon>
            Settings
          </MenuItem>
          <Divider />
          <MenuItem onClick={handleMenuClose}>
            <ListItemIcon>
              <LogoutIcon fontSize="small" />
            </ListItemIcon>
            Logout
          </MenuItem>
        </Menu>
      </div>
    </MainNavigation>
  );
};

export default Header;