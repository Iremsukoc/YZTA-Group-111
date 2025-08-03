import React, { useEffect } from 'react';
import styles from './NotificationToast.module.css';

function NotificationToast({ message, type = 'success', onClose }) {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose();
    }, 3000);

    return () => clearTimeout(timer);
  }, [onClose]);

  const toastTypeStyle = type === 'error' ? styles.error : styles.success;

  return (
    <div className={styles.overlay}>
      <div className={`${styles.toast} ${toastTypeStyle}`}>
        <p>{message}</p>
      </div>
    </div>
  );
}

export default NotificationToast;