import React, { useState, useEffect } from 'react';
import { NavLink, Outlet } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { doc, getDoc } from 'firebase/firestore';
import { db } from '../../firebase.js';
import styles from './ProfilePage.module.css';

function ProfilePage() {
  const { currentUser } = useAuth();
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUserData = async () => {
      if (currentUser) {
        const userDocRef = doc(db, 'users', currentUser.uid);
        const userDoc = await getDoc(userDocRef);
        if (userDoc.exists()) {
          setUserData(userDoc.data());
        } else {
          console.log('Kullanıcı verisi bulunamadı!');
        }
      }
      setLoading(false);
    };

    fetchUserData();
  }, [currentUser]);

  if (loading) {
    return <div className={styles.profileContainer}>Loading...</div>;
  }

  const nameInitial = userData?.first_name ? userData.first_name.charAt(0).toUpperCase() : '';

  return (
    <div className={styles.profileContainer}>
      <header className={styles.profileHeader}>
        <div className={styles.avatar}>{nameInitial}</div>
        <div className={styles.userInfo}>
          <h2>{`${userData?.first_name || ''} ${userData?.last_name || ''}`}</h2>
          <p>{currentUser?.email}</p>
        </div>
      </header>

      <nav className={styles.tabs}>
        <NavLink to="/profile" end className={({ isActive }) => (isActive ? styles.active : '')}>
          Personal Information
        </NavLink>
        <NavLink to="/profile/password" className={({ isActive }) => (isActive ? styles.active : '')}>
          Password & Security
        </NavLink>
      </nav>

      <main>
        {userData && <Outlet context={{ userData, setUserData }} />}
      </main>
    </div>
  );
}

export default ProfilePage;