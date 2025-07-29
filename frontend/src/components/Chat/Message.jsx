import React from 'react';
import styles from './Message.module.css';

function Message({ message }) {
  const isUser = message.role === 'user';


if (message.type === 'diagnosis') {
    const { result, confidence, title = 'Diagnosis' } = message.content || {};
    return (
      <div className={`${styles.message} ${styles.assistant}`}>
        <div className={styles.diagnosisCard}>
          <div className={styles.diagnosisTitle}>{title}</div>
          <div className={styles.diagnosisRow}><strong>Result:</strong> {result ?? '-'}</div>
          <div className={styles.diagnosisRow}><strong>Confidence:</strong> {confidence != null ? `%${confidence}` : '-'}</div>
          {message.content?.note && (
            <div className={styles.diagnosisNote}>{message.content.note}</div>
          )}
        </div>
      </div>
    );
  }


  return (
    <div className={`${styles.message} ${isUser ? styles.user : styles.assistant}`}>
      <div className={styles.bubble}>
        {message.content}
      </div>
    </div>
  );
}

export default Message;
