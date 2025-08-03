import React from 'react';
import { Link } from 'react-router-dom';
import styles from './Header.module.css';
import logoRegAI from '../../assets/logo-regai.png';


function Header() {
  return (
    <header className={styles.header}>
      <div className={styles.logoWrapper}>
        <img className={styles.logoImage} src={logoRegAI} alt="regAI Logo" />
      </div>
      <div className={styles.authButtons}>
        <Link to="/login" className={`${styles.btn} ${styles.btnLogin}`}>Login</Link>
        <Link to="/signup" className={`${styles.btn} ${styles.btnSignup}`}>Sign Up</Link>
      </div>
    </header>
  );
}

export default Header;