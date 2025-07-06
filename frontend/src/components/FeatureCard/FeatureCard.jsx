import React from 'react';
import styles from './FeatureCard.module.css';

function FeatureCard({ icon, title, description }) {
  return (
    <div className={styles.featureCard}>
      <div className={styles.featureIcon}>
        <img src={icon} alt={`${title} Icon`} />
      </div>
      <h2 className={styles.featureTitle}>{title}</h2>
      <p className={styles.featureDescription}>{description}</p>
    </div>
  );
}

export default FeatureCard;