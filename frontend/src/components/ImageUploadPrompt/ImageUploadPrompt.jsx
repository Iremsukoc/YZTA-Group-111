import React, { useRef } from "react";
import styles from "./ImageUploadPrompt.module.css";
import imageIcon from "../../assets/image.svg"; // senin mevcut ikonun

const ImageUploadPrompt = ({ onFileSelect }) => {
  const inputRef = useRef();

  const handleClick = () => {
    inputRef.current.click();
  };

  const handleFileChange = (e) => {
    if (e.target.files.length > 0) {
      onFileSelect(e.target.files[0]);
    }
  };

  return (
    <div className={styles.uploadPrompt} onClick={handleClick}>
      <img src={imageIcon} alt="upload" className={styles.imageIcon} />
      <span className={styles.uploadText}>Görsel yüklemek için tıklayın</span>
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        className={styles.hiddenInput}
        onChange={handleFileChange}
      />
    </div>
  );
};

export default ImageUploadPrompt;
