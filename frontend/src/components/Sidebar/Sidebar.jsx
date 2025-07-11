import React from 'react'; 
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import styles from './Sidebar.module.css';

import dashboardIcon from '../../assets/dashboard-icon.svg';
import myReportsIcon from '../../assets/myreports-icon.svg';
import profileIcon from '../../assets/profile-icon.svg';
import faqIcon from '../../assets/faq-icon.svg';
import logoutIcon from '../../assets/logout-icon.svg';
import helpIcon from '../../assets/help-icon.svg';
import closeIcon from '../../assets/close-icon.svg';

function Sidebar({ isMobileMenuOpen, closeMobileMenu, onOpenMessagePopup }) {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch {
      alert('Failed to log out');
    }
  };

  const handleHelpClick = () => {
    onOpenMessagePopup();
    if (isMobileMenuOpen) {
      closeMobileMenu();
    }
  };

  const handleLinkClick = () => {
    if (isMobileMenuOpen) {
      closeMobileMenu();
    }
  }

  const menuContent = (
    <>
      <div className={styles.logo}>HEALTH</div>
      <ul className={styles.navList}>
        <li className={styles.navItem}>
          <NavLink to="/dashboard" onClick={handleLinkClick} className={({ isActive }) => isActive ? styles.active : ''}>
            <img src={dashboardIcon} alt="Dashboard" className={styles.icon} />
            Dashboard
          </NavLink>
        </li>
        <li className={styles.navItem}>
          <NavLink to="/my-reports" onClick={handleLinkClick} className={({ isActive }) => isActive ? styles.active : ''}>
            <img src={myReportsIcon} alt="My Reports" className={styles.icon} />
            My Reports
          </NavLink>
        </li>
        <li className={styles.navItem}>
          <NavLink to="/profile" onClick={handleLinkClick} className={({ isActive }) => isActive ? styles.active : ''}>
            <img src={profileIcon} alt="Profile" className={styles.icon} />
            Profile
          </NavLink>
        </li>
        <li className={styles.navItem}>
          <NavLink to="/faq" onClick={handleLinkClick} className={({ isActive }) => isActive ? styles.active : ''}>
            <img src={faqIcon} alt="FAQ" className={styles.icon} />
            FAQ
          </NavLink>
        </li>
      </ul>
      <div className={styles.footer}>
        <ul className={styles.navList}>
          <li className={styles.navItem}>
            <a href="#!" onClick={handleHelpClick}>
              <img src={helpIcon} alt="Help" className={styles.icon} />
              Leave us a message
            </a>
          </li>
          <li className={styles.navItem}>
            <a href="#!" onClick={handleLogout}>
              <img src={logoutIcon} alt="Logout" className={styles.icon} />
              Log Out
            </a>
          </li>
        </ul>
      </div>
    </>
  );

  return (
    <>
      <aside className={styles.sidebar}>
        {menuContent}
      </aside>

      <div className={`${styles.mobileOverlay} ${isMobileMenuOpen ? styles.open : ''}`} onClick={closeMobileMenu}>
        <aside className={`${styles.mobileSidebar} ${isMobileMenuOpen ? styles.open : ''}`} onClick={(e) => e.stopPropagation()}>
          <div className={styles.closeButtonContainer}>
            <button className={styles.closeButton} onClick={closeMobileMenu}>
              <img src={closeIcon} alt="Close menu" />
            </button>
          </div>
          {menuContent}
        </aside>
      </div>
    </>
  );
}

export default Sidebar;