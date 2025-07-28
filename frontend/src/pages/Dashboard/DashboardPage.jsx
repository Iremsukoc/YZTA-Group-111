import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import styles from './DashboardPage.module.css';
import ResumeModal from '../../components/ResumeModal/ResumeModal';

function DashboardPage() {
  const { currentUser } = useAuth();
  const navigate = useNavigate();
  const firstName = currentUser?.reloadUserInfo?.customAttributes ? JSON.parse(currentUser.reloadUserInfo.customAttributes).firstName : 'User';

  const [ongoingAssessments, setOngoingAssessments] = useState([]);
  const [isModalOpen, setModalOpen] = useState(false);

  useEffect(() => {
    const fetchOngoingAssessments = async () => {
      if (!currentUser) return;
      try {
        const token = await currentUser.getIdToken();
        const response = await fetch('http://127.0.0.1:8000/assessments?status=in_progress', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.ok) {
          const data = await response.json();
          setOngoingAssessments(data);
        }
      } catch (error) {
        console.error("Failed to fetch ongoing assessments:", error);
      }
    };
    fetchOngoingAssessments();
  }, [currentUser]);

  const handleStartNew = async () => {
    try {
      const token = await currentUser.getIdToken();
      const response = await fetch('http://127.0.0.1:8000/assessments', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ assessment_type: "general_test" })
      });

      if (!response.ok) {
        throw new Error("Failed to start a new assessment session.");
      }

      const data = await response.json();
      navigate(`/assessment/${data.assessment_id}`);

    } catch (error) {
      console.error("Error starting new assessment:", error);
      alert("Could not start a new assessment. Please try again later.");
    }
  };

  const handleSmartButton = () => {
    if (ongoingAssessments.length > 0) {
      setModalOpen(true);
    } else {
      handleStartNew();
    }
  };

  return (
    <>
      <div className={styles.dashboardContainer}>
        <section className={styles.welcomeHeader}>
          <h2>Welcome back, {firstName}</h2>
          <p>Ready to start a new health assessment ?</p>
          <button onClick={handleSmartButton} className={styles.newAssessmentBtn}>
            Start Health Assessment
          </button>
        </section>

        <section className={styles.assessmentsList}>
        </section>
      </div>
      <ResumeModal 
        isOpen={isModalOpen} 
        onClose={() => setModalOpen(false)} 
        assessments={ongoingAssessments}
        onStartNew={handleStartNew}
      />
    </>
  );
}

export default DashboardPage;