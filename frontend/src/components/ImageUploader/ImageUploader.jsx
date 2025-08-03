import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import styles from './ImageUploader.module.css';
import NotificationToast from '../NotificationToast/NotificationToast';

function ImageUploader({ assessmentId, onUploadComplete }) {
  const { currentUser } = useAuth();
  const [selectedFile, setSelectedFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [popup, setPopup] = useState({ show: false, message: '', type: '' });

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setPopup({ show: true, message: 'Please select an image file first.', type: 'error' });
      return;
    }
    setIsLoading(true);

    const formData = new FormData();
    formData.append('image_file', selectedFile);
    
    try {
      const token = await currentUser.getIdToken();


      const response = await fetch(`http://127.0.0.1:8000/assessments/${assessmentId}/image`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });

      const result = await response.json();
      
      if (!response.ok) {
        throw new Error(result.detail || 'Image analysis failed.');
      }
      
      setPopup({ show: true, message: 'Image analyzed successfully!', type: 'success' });
      onUploadComplete(result);

    } catch (error) {
      setPopup({ show: true, message: error.message, type: 'error' });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.uploaderContainer}>
      {popup.show && (
        <NotificationToast
          message={popup.message}
          type={popup.type}
          onClose={() => setPopup({ show: false, message: '', type: '' })}
        />
      )}
      <p className={styles.instruction}>The final step is image analysis. Please upload your medical image.</p>
      <div className={styles.fileInputWrapper}>
        <input type="file" id="imageUpload" accept="image/png, image/jpeg" onChange={handleFileChange} />
        <label htmlFor="imageUpload" className={styles.fileInputLabel}>
          {selectedFile ? selectedFile.name : 'Choose a file...'}
        </label>
      </div>
      <button onClick={handleUpload} disabled={isLoading || !selectedFile} className={styles.uploadButton}>
        {isLoading ? 'Analyzing...' : 'Upload and Analyze'}
      </button>
    </div>
  );
}

export default ImageUploader;