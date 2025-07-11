import React, { useState } from 'react';
import styles from './PasswordPage.module.css';
import eyeIcon from '../../assets/eye-icon.svg';

function PasswordPage() {
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmNewPassword, setConfirmNewPassword] = useState('');

  const [currentPasswordVisible, setCurrentPasswordVisible] = useState(false);
  const [newPasswordVisible, setNewPasswordVisible] = useState(false);
  const [confirmPasswordVisible, setConfirmPasswordVisible] = useState(false);

  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChangePassword = async (e) => {
    e.preventDefault();
    setError('');

    if (newPassword !== confirmNewPassword) {
      return setError('New passwords do not match.');
    }
    if (newPassword.length < 8) {
      return setError('New password must be at least 8 characters long.');
    }

    setLoading(true);
    alert('Password would be changed here!');
    setLoading(false);
  };

  return (
    <div className={styles.passwordContainer}>
      <div className={styles.header}>
        <h2>Password & Security</h2>
      </div>

      {error && <div className={styles.errorMessage}>{error}</div>}

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