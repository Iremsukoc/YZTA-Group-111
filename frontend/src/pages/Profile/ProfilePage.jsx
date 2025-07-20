import React from 'react';
import { NavLink, Outlet } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import styles from './ProfilePage.module.css';

function ProfilePage() {
  const { currentUser } = useAuth();
  const claims = currentUser?.reloadUserInfo?.customAttributes ? JSON.parse(currentUser.reloadUserInfo.customAttributes) : {};
  const initialFirstName = claims.firstName || 'User';
  const initialLastName = claims.lastName || '';
  const nameInitial = initialFirstName.charAt(0).toUpperCase();

  return (
    <div className={styles.profileContainer}>
      <header className={styles.profileHeader}>
        <div className={styles.avatar}>{nameInitial}</div>
        <div className={styles.userInfo}>
          <h2>{`${initialFirstName} ${initialLastName}`}</h2>
          <p>{currentUser?.email}</p>
        </div>
      </header>

      <nav className={styles.tabs}>
        <NavLink to="/profile" end className={({ isActive }) => isActive ? styles.active : ''}>
          Personal Information
        </NavLink>
        <NavLink to="/profile/password" className={({ isActive }) => isActive ? styles.active : ''}>
          Password & Security
        </NavLink>
      </nav>

      <Outlet />
    </div>
  );
}

export default ProfilePage;