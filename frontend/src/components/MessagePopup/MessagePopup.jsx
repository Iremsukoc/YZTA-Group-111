import React, { useState } from 'react';
import styles from './MessagePopup.module.css';
import attachmentIcon from '../../assets/attachment-icon.svg';
import { useAuth } from '../../context/AuthContext';

function MessagePopup({ isOpen, onClose }) {
  const { currentUser } = useAuth();

  const [email, setEmail] = useState(currentUser?.email || '');
  const [message, setMessage] = useState('');

  if (!isOpen) {
    return null;
  }

  const handleFormSubmit = (e) => {
    e.preventDefault();
    alert(`Message from ${email} would be sent here!`);
    onClose();
  };

  const stopPropagation = (e) => e.stopPropagation();

  return (
    <div className={styles.popup} onClick={stopPropagation}>
      <header className={styles.popupHeader}>
        Leave us a message
        <button className={styles.closeButton} onClick={onClose}>&times;</button>
      </header>
      <div className={styles.popupContent}>
        <form onSubmit={handleFormSubmit}>
          <div className={styles.formGroup}>
            <label className={styles.formLabel} htmlFor="email">Your email address</label>
            <input 
              type="email" 
              id="email" 
              className={styles.formInput} 
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className={styles.formGroup}>
            <label className={styles.formLabel} htmlFor="message">How can we help you?</label>
            <textarea 
              id="message" 
              className={styles.formTextarea}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              required
            ></textarea>
          </div>
          <div className={styles.formGroup}>
            <label className={styles.formLabel}>Attachments</label>
            <div className={styles.attachmentBox}>
              <img src={attachmentIcon} alt="attachment" />
              Upload up to 2 files
            </div>
          </div>
          <div className={styles.buttonWrapper}>
  <         button type="submit" className={styles.sendButton}>Send Message</button>
          </div>        
        </form>
      </div>
    </div>
  );
}

export default MessagePopup;