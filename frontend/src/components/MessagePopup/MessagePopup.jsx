import React, { useState } from 'react';
import styles from './MessagePopup.module.css';
import attachmentIcon from '../../assets/attachment-icon.svg';
import { useAuth } from '../../context/AuthContext';

function MessagePopup({ isOpen, onClose }) {
  const { currentUser } = useAuth();

  const [email, setEmail] = useState(currentUser?.email || '');
  const [message, setMessage] = useState('');
  const [file, setFile] = useState(null);
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  if (!isOpen) return null;

  const handleFormSubmit = async (e) => {
    e.preventDefault();
  
    const formData = new FormData();
    formData.append("email", email);
    formData.append("message", message);
    if (file) {
      formData.append("attachment", file);
    }
  
    try {
      const res = await fetch("https://formspree.io/f/xdkddwek", {
        method: "POST",
        body: formData,
        mode: 'no-cors', // Disable CORS checks for this request
        redirect: 'follow' // Required when using no-cors mode
      });
  
      // With no-cors mode, we can't read the response status, but if we reach here
      // without an error, the request was likely successful
      setSuccessMessage("Your message has been sent successfully!");
      setMessage("");
      setFile(null);
      setTimeout(() => {
        setSuccessMessage("");
        onClose();
      }, 3000);
    } catch (err) {
      console.error("Unexpected error:", err);
      setErrorMessage("An unexpected error occurred.");
      setTimeout(() => setErrorMessage(""), 3000);
    }
  };
  

  const stopPropagation = (e) => e.stopPropagation();

  return (
    <div className={styles.popup} onClick={stopPropagation}>
      <header className={styles.popupHeader}>
        Leave us a message
        <button className={styles.closeButton} onClick={onClose}>&times;</button>
      </header>
      <div className={styles.popupContent}>
        <form onSubmit={handleFormSubmit} encType="multipart/form-data">
          <div className={styles.formGroup}>
            <label className={styles.formLabel} htmlFor="email">Sender Email</label>
            <input
              type="email"
              id="email"
              className={styles.formInput}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              name="email"
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
              name="message"
            ></textarea>
          </div>
          <div className={styles.formGroup}>
            <label className={styles.formLabel}>Attachments (optional)</label>
            <label className={styles.attachmentBox}>
              <img src={attachmentIcon} alt="attachment" />
              Upload a file
              <input
                type="file"
                name="attachment"
                onChange={(e) => setFile(e.target.files[0])}
                style={{ display: 'none' }}
              />
            </label>
          </div>
          <div className={styles.buttonWrapper}>
            <button type="submit" className={styles.sendButton}>Send Message</button>
          </div>
        </form>

        {/* Toast messages */}
        {successMessage && (
          <div className={styles.successToast}>
            {successMessage}
          </div>
        )}
        {errorMessage && (
          <div className={styles.errorToast}>
            {errorMessage}
          </div>
        )}
      </div>
    </div>
  );
}

export default MessagePopup;
