import React from 'react';
import styles from './DashboardPage.module.css';
import searchIcon from '../../assets/search-icon.svg';
import detailedIcon from '../../assets/detailed-icon.svg';
import imageIcon from '../../assets/image.svg';



function DashboardPage() {
  return (
    <div className={styles.cardGrid}>
      <div className={styles.card}>
        <img src={searchIcon} alt="" className={styles.cardIcon} />
        <h3>General Evaluation</h3>
        <p>We determine the most likely type of cancer with a short test based on your complaint.</p>
        <button className={styles.actionButton}>Start General Test</button>
      </div>

      <div className={styles.card}>
        <img src={detailedIcon} alt="" className={styles.cardIcon} />
        <h3>Detailed Analysis</h3>
        <p>Get data-detailed risk prediction with AI support.</p>
        <button className={styles.actionButton}>Start Detailed Analysis</button>
      </div>

      <div className={styles.bottomCardWrapper}>
        <div className={styles.card}>
          <img src={imageIcon} alt="" className={styles.cardIcon} />
          <h3>Image Processing</h3>
          <p>Upload your medical images for advanced analysis.</p>
          <button className={styles.actionButton}>Upload Image</button>
        </div>
      </div>
    </div>
  
  );
}

export default DashboardPage;