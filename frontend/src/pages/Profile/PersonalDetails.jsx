import React, { useState, useEffect } from 'react';
import { useOutletContext } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext.jsx';
import styles from './ProfilePage.module.css';
import { doc, updateDoc } from 'firebase/firestore';
import { db } from '../../firebase.js';

import NotificationToast from '../../components/NotificationToast/NotificationToast.jsx';

function PersonalDetails() {
  const { userData, setUserData } = useOutletContext();
  const { currentUser } = useAuth();
  const [formData, setFormData] = useState(userData);
  const [popup, setPopup] = useState({ show: false, message: '', type: '' });

  useEffect(() => {
    setFormData(userData);
  }, [userData]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSaveChanges = async (e) => {
    e.preventDefault();
    if (!currentUser) {
      setPopup({ show: true, message: 'You must be logged in.', type: 'error' });
      return;
    }

    try {
      const token = await currentUser.getIdToken();
      const response = await fetch('http://127.0.0.1:8000/users/me', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Failed to update profile.');
      }
      
      setUserData(formData);
      setPopup({ show: true, message: 'Profile updated successfully!', type: 'success' });

    } catch (err) {
      setPopup({ show: true, message: err.message, type: 'error' });
    }
  };

  const handleDeleteAccount = async () => {
    if (!window.confirm('Are you sure you want to delete your account? This action cannot be undone.')) return;
    
    if (!currentUser) {
        setPopup({ show: true, message: 'You must be logged in.', type: 'error' });
        return;
    }

    try {
      const token = await currentUser.getIdToken();
      const response = await fetch('http://127.0.0.1:8000/users/me', {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Failed to delete account.');
      }

      setPopup({ show: true, message: 'Account deleted successfully. You will be logged out.', type: 'success' });
      
      setTimeout(() => {
        window.location.href = '/login'; 
      }, 3000);

    } catch (err) {
      setPopup({ show: true, message: err.message, type: 'error' });
    }
  };

  if (!formData) return <div>Loading...</div>;

  return (
    <>
      {popup.show && (
        <NotificationToast
          message={popup.message}
          type={popup.type}
          onClose={() => setPopup({ show: false, message: '', type: '' })}
        />
      )}

      <form onSubmit={handleSaveChanges}>
        <div className={styles.formGrid}>
          <div className={styles.formGroup}>
            <label className={styles.formLabel}>First Name</label>
            <input type="text" name="first_name" className={styles.formInput} value={formData.first_name || ''} onChange={handleInputChange} />
          </div>
          <div className={styles.formGroup}>
            <label className={styles.formLabel}>Last Name</label>
            <input type="text" name="last_name" className={styles.formInput} value={formData.last_name || ''} onChange={handleInputChange} />
          </div>
          <div className={styles.formGroup}>
            <label className={styles.formLabel}>Email Address</label>
            <input type="email" className={styles.formInput} value={currentUser.email || ''} disabled />
          </div>
          <div className={styles.formGroup}>
            <label className={styles.formLabel}>Phone Number</label>
            <input type="tel" name="phone_number" className={styles.formInput} value={formData.phone_number || ''} onChange={handleInputChange} placeholder="Enter your phone number" />
          </div>
          <div className={styles.formGroup}>
            <label className={styles.formLabel}>Date of Birth</label>
            <input type="date" name="dob" className={styles.formInput} value={formData.dob || ''} onChange={handleInputChange} />
          </div>
          <div className={styles.formGroup}>
            <label className={styles.formLabel}>Gender</label>
            <select name="gender" className={styles.formInput} value={formData.gender || ''} onChange={handleInputChange}>
              <option value="" disabled>Select gender</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Prefer not to say">Rather not say</option>
            </select>
          </div>
          <div className={styles.formActions}>
            <button type="submit" className={styles.saveButton}>Save Changes</button>
          </div>
        </div>
      </form>

      <section className={styles.deleteSection}>
        <div className={styles.deleteInfo}>
          <h3>Delete Account</h3>
          <p>Once you delete your account, there is no going back. Please be certain.</p>
        </div>
        <button type="button" className={styles.deleteButton} onClick={handleDeleteAccount}>Delete my account</button>
      </section>
    </>
  );
}

export default PersonalDetails;