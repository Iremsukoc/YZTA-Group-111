import React from 'react';
import styles from './ReportCard.module.css';
import lungIcon from '../../assets/profile-icon.svg';

function ReportCard({ report }) {
  const { title, date, riskLevel } = report;

  const getRiskClass = () => {
    if (riskLevel === 'High') return styles.highRisk;
    if (riskLevel === 'Medium') return styles.mediumRisk;
    return styles.lowRisk;
  };

  return (
    <div className={styles.card}>
      <div className={styles.iconContainer}>
        <img src={lungIcon} alt="" className={styles.icon} />
      </div>
      <div className={styles.info}>
        <h4 className={styles.title}>{title}</h4>
        <p className={styles.date}>{date}</p>
      </div>
      <div className={`${styles.risk} ${getRiskClass()}`}>
        <span className={styles.riskDot}></span>
        {riskLevel} Risk
      </div>
    </div>
  );
}

export default ReportCard;
