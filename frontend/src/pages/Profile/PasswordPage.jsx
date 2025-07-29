import React, { useState } from 'react';
import styles from './PasswordPage.module.css';
import eyeIcon from '../../assets/eye-icon.svg';
import { useAuth } from '../../context/AuthContext';
import NotificationToast from '../../components/NotificationToast/NotificationToast.jsx';


function PasswordPage() {
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmNewPassword, setConfirmNewPassword] = useState('');

  const [currentPasswordVisible, setCurrentPasswordVisible] = useState(false);
  const [newPasswordVisible, setNewPasswordVisible] = useState(false);
  const [confirmPasswordVisible, setConfirmPasswordVisible] = useState(false);

  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [popup, setPopup] = useState({ show: false, message: '', type: '' });


  const { currentUser } = useAuth();

  const handleChangePassword = async (e) => {
    e.preventDefault();

    if (newPassword !== confirmNewPassword) {
      return setError('New passwords do not match.');
    }
    if (newPassword.length < 8) {
      return setError('New password must be at least 8 characters long.');
    }

    setLoading(true);
    try {
      const token = await currentUser.getIdToken();
      const response = await fetch('http://127.0.0.1:8000/users/me/change-password', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword
        })
      });
      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Failed to change password.');
      }
      setPopup({ show: true, message: 'Password changed successfully!', type: 'success' });
      setCurrentPassword('');
      setNewPassword('');
      setConfirmNewPassword('');
    } catch (err) {
      setPopup({ show: true, message: err.message, type: 'error' });
    }
    setLoading(false);
  };

  return (
    <div className={styles.passwordContainer}>
      {popup.show && (
        <NotificationToast
          message={popup.message}
          type={popup.type}
          onClose={() => setPopup({ show: false, message: '', type: '' })}
        />
      )}
      <div className={styles.header}>
        <h2>Password & Security</h2>
      </div>


      <form onSubmit={handleChangePassword} className={styles.form}>
        <div className={styles.formGroup}>
          <label className={styles.formLabel}>Current Password</label>
          <div className={styles.passwordWrapper}>
            <input
              type={currentPasswordVisible ? 'text' : 'password'}
              className={styles.formInput}
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
              placeholder="Enter your current password"
            />
            <button type="button" className={styles.passwordToggle} onClick={() => setCurrentPasswordVisible(!currentPasswordVisible)}>
              <img src={eyeIcon} alt="Toggle visibility" />
            </button>
          </div>
        </div>

        <div className={styles.formGroup}>
          <label className={styles.formLabel}>New Password</label>
          <div className={styles.passwordWrapper}>
            <input
              type={newPasswordVisible ? 'text' : 'password'}
              className={styles.formInput}
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              placeholder="Enter your new password"
            />
            <button type="button" className={styles.passwordToggle} onClick={() => setNewPasswordVisible(!newPasswordVisible)}>
              <img src={eyeIcon} alt="Toggle visibility" />
            </button>
          </div>
        </div>

        <div className={styles.formGroup}>
          <label className={styles.formLabel}>Confirm New Password</label>
          <div className={styles.passwordWrapper}>
            <input
              type={confirmPasswordVisible ? 'text' : 'password'}
              className={styles.formInput}
              value={confirmNewPassword}
              onChange={(e) => setConfirmNewPassword(e.target.value)}
              placeholder="Confirm your new password"
            />
            <button type="button" className={styles.passwordToggle} onClick={() => setConfirmPasswordVisible(!confirmPasswordVisible)}>
              <img src={eyeIcon} alt="Toggle visibility" />
            </button>
          </div>
        </div>
        
        <div className={styles.formActions}>
          <button type="submit" className={styles.changeButton} disabled={loading}>
            {loading ? 'Saving...' : 'Change Password'}
          </button>
        </div>
      </form>
    </div>
  );
}

export default PasswordPage;