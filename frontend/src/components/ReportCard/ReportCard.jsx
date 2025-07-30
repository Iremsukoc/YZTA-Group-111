import React from 'react';
import styles from './ReportCard.module.css';
import lungIcon from '../../assets/profile-icon.svg';
import { useNavigate } from 'react-router-dom';

function ReportCard({ report }) {
  const { title, date, riskLevel, status, id, confidence } = report;
  const navigate = useNavigate();

  const handleClick = () => {
    navigate(`/assessment/${id}`);
  };

  const getRiskClass = () => {
    if (riskLevel === 'High') return styles.highRisk;
    if (riskLevel === 'Medium') return styles.mediumRisk;
    return styles.lowRisk;
  };

  return (
    <div className={styles.card} onClick={handleClick}>
      <div className={styles.iconContainer}>
        <img src={lungIcon} alt="icon" className={styles.icon} />
      </div>
      <div className={styles.info}>
        <h4 className={styles.title}>{title}</h4>
        <p className={styles.date}>{date}</p>
      </div>
      {status !== 'completed' && (
        <span className={styles.incompleteBadge}>In progress</span>
      )}
      {status === 'completed' ? (
        <div className={`${styles.risk} ${getRiskClass()}`}>
          <span className={styles.riskDot}></span>
          {riskLevel} Risk

        </div>
      ) : (
        <button className={styles.continueBtn} type="button">
          Continue
        </button>
      )}
    </div>
  );
}

export default ReportCard;

