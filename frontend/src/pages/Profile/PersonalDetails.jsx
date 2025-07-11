import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import styles from './ProfilePage.module.css';

function PersonalDetails() {
  const { currentUser } = useAuth();
  const claims = currentUser?.reloadUserInfo?.customAttributes ? JSON.parse(currentUser.reloadUserInfo.customAttributes) : {};
  const initialFirstName = claims.firstName || 'User';
  const initialLastName = claims.lastName || '';
  const initialEmail = currentUser?.email || '';

  const [firstName, setFirstName] = useState(initialFirstName);
  const [lastName, setLastName] = useState(initialLastName);
  const [phone, setPhone] = useState('');
  const [dob, setDob] = useState('');
  const [gender, setGender] = useState('');

  const handleSaveChanges = (e) => {
    e.preventDefault();
    alert('Profile changes would be saved here!');
  };

  const handleDeleteAccount = () => {
    if (window.confirm('Are you sure you want to delete your account?')) {
      alert('Account would be deleted here!');
    }
  };

  return (
    <>
      <form onSubmit={handleSaveChanges}>
        <div className={styles.formGrid}>
          <div className={styles.formGroup}>
            <label className={styles.formLabel}>First Name</label>
            <input type="text" className={styles.formInput} value={firstName} onChange={e => setFirstName(e.target.value)} />
          </div>
          <div className={styles.formGroup}>
            <label className={styles.formLabel}>Last Name</label>
            <input type="text" className={styles.formInput} value={lastName} onChange={e => setLastName(e.target.value)} />
          </div>
          <div className={styles.formGroup}>
            <label className={styles.formLabel}>Email Address</label>
            <input type="email" className={styles.formInput} value={initialEmail} disabled />
          </div>
          <div className={styles.formGroup}>
            <label className={styles.formLabel}>Phone Number</label>
            <input type="tel" className={styles.formInput} value={phone} onChange={e => setPhone(e.target.value)} placeholder="Enter your phone number" />
          </div>
          <div className={styles.formGroup}>
            <label className={styles.formLabel}>Date of Birth</label>
            <input type="date" className={styles.formInput} value={dob} onChange={e => setDob(e.target.value)} />
          </div>
          <div className={styles.formGroup}>
            <label className={styles.formLabel}>Gender</label>
            <input type="text" className={styles.formInput} value={gender} onChange={e => setGender(e.target.value)} placeholder="Your gender" />
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
        <button className={styles.deleteButton} onClick={handleDeleteAccount}>Delete my account</button>
      </section>
    </>
  );
}

export default PersonalDetails;