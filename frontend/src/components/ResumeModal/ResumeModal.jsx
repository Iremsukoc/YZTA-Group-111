import React from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './ResumeModal.module.css';

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
    if (!timestamp || !timestamp.seconds) {
      return 'Invalid Date';
    }
    return new Date(timestamp.seconds * 1000).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
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
            assessments.map(asmnt => (
              <div key={asmnt.assessment_id} className={styles.assessmentCard} onClick={() => handleResume(asmnt.assessment_id)}>
                <div className={styles.assessmentInfo}>
                  <p><strong>{asmnt.assessmentType?.replace('_', ' ') || 'Unknown Type'}</strong></p>
                  <p>{formatDate(asmnt.createdAt)}</p>
                </div>
              </div>
            ))
          ) : (
            <p>No ongoing assessments found.</p>
          )}
        </div>

        <div className={styles.actions}>
          <button onClick={handleStartNewAnyway} className={styles.startNewButton}>
            Start a New Assessment Anyway
          </button>
        </div>
      </div>
    </div>
  );
}

export default ResumeModal;