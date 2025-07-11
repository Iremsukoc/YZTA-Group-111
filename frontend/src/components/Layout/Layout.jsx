import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from '../Sidebar/Sidebar';
import MessagePopup from '../MessagePopup/MessagePopup';
import styles from './Layout.module.css';

import hamburgerIcon from '../../assets/hamburger-icon.svg';

const MobileHeader = ({ onMenuClick }) => (
  <header className={styles.mobileHeader}>
    <div className={styles.logo}>HEALTH</div>
    <button className={styles.hamburgerButton} onClick={onMenuClick}>
      <img src={hamburgerIcon} alt="Open menu" />
    </button>
  </header>
);

function Layout() {
  const [isMessagePopupOpen, setIsMessagePopupOpen] = useState(false);
  const [isMobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleOpenPopup = () => {
    setMobileMenuOpen(false); 
    setIsMessagePopupOpen(true);
  };

  const handleClosePopup = () => setIsMessagePopupOpen(false);

  return (
    <div className={styles.appContainer}>
   
      <Sidebar 
        isMobileMenuOpen={isMobileMenuOpen} 
        closeMobileMenu={() => setMobileMenuOpen(false)} 
        onOpenMessagePopup={handleOpenPopup}
      />
      
      <div className={styles.mainContentWrapper}>
        <MobileHeader onMenuClick={() => setMobileMenuOpen(true)} />
        <main className={styles.content}>
          <Outlet /> 
        </main>
      </div>
      
      <MessagePopup 
        isOpen={isMessagePopupOpen} 
        onClose={handleClosePopup} 
      />
    </div>
  );
}

export default Layout;