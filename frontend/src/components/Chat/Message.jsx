import React from 'react';
import styles from './Message.module.css';

function Message({ message }) {
  const isUser = message.role === 'user';
  return (
    <div className={`${styles.message} ${isUser ? styles.user : styles.assistant}`}>
      <div className={styles.bubble}>
        {message.content}
      </div>
    </div>
  );
}

export default Message;