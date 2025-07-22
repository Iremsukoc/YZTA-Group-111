import React, { useState, useRef, useEffect } from 'react';
import styles from './ChatInput.module.css';
import plusIcon from '../../assets/plus-icon.svg'; 
import microphoneIcon from '../../assets/microphone-icon.svg';
import sendIcon from '../../assets/send-icon.svg';

function ChatInput({ onSendMessage, isLoading }) {
  const [inputValue, setInputValue] = useState('');
  const textareaRef = useRef(null);

  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${textarea.scrollHeight}px`;
    }
  }, [inputValue]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputValue.trim() && !isLoading) {
      onSendMessage(inputValue);
      setInputValue('');
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const hasText = inputValue.trim().length > 0;

  return (
    <div className={styles.inputContainer}>
      <form className={`${styles.inputForm} ${hasText ? styles.hasText : ''}`} onSubmit={handleSubmit}>
        <textarea
          ref={textareaRef}
          className={styles.textInput}
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="How can I help you with your health concerns today?"
          disabled={isLoading}
          rows={1}
        />

        <div className={styles.footer}>
          <button type="button" className={styles.iconButton} onClick={() => alert('File upload will be implemented!')}>
            <img src={plusIcon} alt="Attach file" />
          </button>
          
          <div className={styles.rightButtonsContainer}>
            <button 
              type="button" 
              className={`${styles.iconButton} ${styles.microphoneButton}`} 
              disabled={isLoading} 
              onClick={() => alert('Voice input will be implemented!')}
              aria-label="Use microphone"
            >
              <img src={microphoneIcon} alt="Use microphone" />
            </button>
            <button 
              type="submit" 
              className={styles.sendButton} 
              disabled={isLoading || !hasText}
              aria-label="Send message"
            >
              <img src={sendIcon} alt="Send" />
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}

export default ChatInput;