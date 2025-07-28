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

  return (
    <div className={styles.overlay} onClick={onClose}>
      <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
        <h3>Ongoing Assessments</h3>
        <div className={styles.assessmentList}>
          {assessments.map(asmnt => (
            <div key={asmnt.id} className={styles.assessmentCard} onClick={() => handleResume(asmnt.id)}>
              <p><strong>{asmnt.assessmentType.replace('_', ' ')}</strong></p>
              <p>{new Date(asmnt.createdAt.seconds * 1000).toLocaleDateString()}</p>
            </div>
          ))}
        </div>
        <button onClick={handleStartNewAnyway}>Start a New Assessment Anyway</button>
      </div>
    </div>
  );
}

export default ResumeModal;