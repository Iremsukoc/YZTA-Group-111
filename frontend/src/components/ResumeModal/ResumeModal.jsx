import React from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './ResumeModal.module.css';
import profileIcon from '../../assets/profile-icon.svg';


function ResumeModal({ isOpen, onClose, assessments, onStartNew }) {
  const navigate = useNavigate();

  if (!isOpen) return null;

  const handleResume = (id) => {
    navigate(`/assessment/${id}`);
    onClose();
  };

  const handleStartNewAnyway = () => {
    onStartNew();
    onClose();
  };

  const formatDate = (timestamp) => {
    if (!timestamp) return 'Invalid Date';
    try {
      const date = new Date(timestamp);
      if (isNaN(date.getTime())) return 'Invalid Date';
      return date.toLocaleDateString('tr-TR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
      });
    } catch (error) {
      return 'Invalid Date';
    }
  };

  return (
    <div className={styles.overlay} onClick={onClose}>
      <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
        <div className={styles.modalHeader}>
          <h3>Ongoing Assessments</h3>
          <button onClick={onClose} className={styles.closeButton}>&times;</button>
        </div>

        <div className={styles.assessmentList}>
          {assessments && assessments.length > 0 ? (
            assessments.map((asmnt) => {
              const title =
                asmnt.title ||
                asmnt.assessment_type?.replace('_', ' ') ||
                'Unknown Type';

              return (
                <div
                  key={asmnt.assessment_id}
                  className={styles.reportCard}
                  onClick={() => handleResume(asmnt.assessment_id)}
                >
                  <div className={styles.cardIcon}>
                    <img src={profileIcon} alt="icon" />
                  </div>
                  <div className={styles.cardContent}>
                    <div className={styles.cardTitle}>{title}</div>
                    <div className={styles.cardDate}>
                      {formatDate(asmnt.created_at)}
                    </div>
                  </div>
                  <div className={styles.cardStatus}>
                    <span className={styles.statusBadge}>In progress</span>
                    <button className={styles.continueButton}>Continue</button>
                  </div>
                </div>
              );
            })
          ) : (
            <p>No ongoing assessments found.</p>
          )}
        </div>

        <div className={styles.actions}>
          <button onClick={handleStartNewAnyway} className={styles.startNewButton}>
            Start New Assessment
          </button>
        </div>
      </div>
    </div>
  );
}

export default ResumeModal;

