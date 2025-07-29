import React, { useState, useRef, useEffect } from 'react';
import styles from './ChatInput.module.css';
import plusIcon from '../../assets/plus-icon.svg'; 
import microphoneIcon from '../../assets/microphone-icon.svg';
import sendIcon from '../../assets/send-icon.svg';


function ChatInput({ onSendMessage, onImageSelected, isLoading, isImageUploadAllowed }) {
  const [inputValue, setInputValue] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const textareaRef = useRef(null);
  const InputRef = useRef(null);
  const uploadButtonRef = useRef(null);
  const [showUploadMenu, setShowUploadMenu] = useState(false);

  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${textarea.scrollHeight}px`;
    }
  }, [inputValue]);

  useEffect(() => {
    if (!isLoading && textareaRef.current) {
     textareaRef.current.focus();
    }
  }, [isLoading]);
    

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (isLoading) return;
  
    if (selectedFile) {
      if (onImageSelected) {
        await onImageSelected(selectedFile);
      }
      setSelectedFile(null);
      setInputValue('');
    } 
    else if (inputValue.trim()) {
      onSendMessage(inputValue);
      setInputValue('');
      if (textareaRef.current) {
        textareaRef.current.focus();
      }
    }
  };
  

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
      if (textareaRef.current) {
        textareaRef.current.focus();
      }
    }
  };

  const handleUploadClick = () => {
    fileInputRef.current?.click();
    setShowUploadMenu(false);
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setInputValue(`Seçilen dosya: ${file.name}`);
    }
  };
  
  const hasText = inputValue.trim().length > 0;

  return (
    <div className={styles.inputContainer} style={{ position: 'relative' }}>
      {isImageUploadAllowed ? (
        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          className={styles.visibleFileInput}
          disabled={isLoading}
        />
      ) : (
        <input
          type="file"
          accept="image/*"
          ref={InputRef}
          style={{ display: 'none' }}
          onChange={handleFileChange}
          disabled={isLoading}
        />
      )}


      {showUploadMenu && (
        <div
          className={styles.uploadMenu}
          style={{
            position: 'absolute',
            bottom: 60,
            left: uploadButtonRef.current?.offsetLeft || 0,
          }}
        >
          <button
            type="button"
            onClick={handleUploadClick}
            disabled={isLoading || !isImageUploadAllowed} 
          >
            📎 Fotoğraf veya dosya ekle
          </button>
        </div>
      )}

      <form className={`${styles.inputForm} ${hasText ? styles.hasText : ''}`} onSubmit={handleSubmit}>
        <textarea
          ref={textareaRef}
          className={styles.textInput}
          value={inputValue}
          onChange={(e) => !selectedFile && setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="How can I help you with your health concerns today?"
          disabled={isLoading} 
          rows={1}
        />

        <div className={styles.footer}>
          <button
            type="button"
            className={styles.iconButton}
            onClick={() => setShowUploadMenu(prev => !prev)}
            ref={uploadButtonRef}
          >
            <img src={plusIcon} alt="Attach file" />
          </button>
          
          <div className={styles.rightButtonsContainer}>
            <button 
              type="button" 
              className={`${styles.iconButton} ${styles.microphoneButton}`} 
              disabled={isLoading} 
            >
              <img src={microphoneIcon} alt="Use microphone" />
            </button>
            <button 
              type="submit" 
              className={styles.sendButton} 
              disabled={isLoading || (!hasText && !selectedFile)}
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