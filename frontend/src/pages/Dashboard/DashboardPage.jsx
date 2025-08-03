import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { doc, getDoc } from 'firebase/firestore';
import { db } from '../../firebase.js';
import styles from './DashboardPage.module.css';
import ResumeModal from '../../components/ResumeModal/ResumeModal';

function DashboardPage() {
  const { currentUser } = useAuth();
  const navigate = useNavigate();
  const [userData, setUserData] = useState(null);
  const [ongoingAssessments, setOngoingAssessments] = useState([]);
  const [isModalOpen, setModalOpen] = useState(false);

  // Fetch user data from Firestore
  useEffect(() => {
    const fetchUserData = async () => {
      if (currentUser) {
        const userDocRef = doc(db, 'users', currentUser.uid);
        const userDoc = await getDoc(userDocRef);
        if (userDoc.exists()) {
          setUserData(userDoc.data());
        }
      }
    };
    fetchUserData();
  }, [currentUser]);

  // Fallback to Firebase Auth custom attributes if Firestore data is not available
  const firstName = userData?.first_name || (currentUser?.reloadUserInfo?.customAttributes ? JSON.parse(currentUser.reloadUserInfo.customAttributes).firstName : 'User');

  useEffect(() => {
    const fetchOngoingAssessments = async () => {
      if (!currentUser) return;
      try {
        const token = await currentUser.getIdToken();
        const response = await fetch('http://127.0.0.1:8000/assessments/report_summaries', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.ok) {
          const data = await response.json();
          const ongoing = data.filter(assessment => assessment.status !== 'completed');
          setOngoingAssessments(ongoing);
        }
      } catch (error) {
        console.error("Failed to fetch ongoing assessments:", error);
      }
    };
    fetchOngoingAssessments();
  }, [currentUser]);

  const handleStartNew = async () => {
    try {
      if (!currentUser) {
        throw new Error("User not authenticated.");
      }      
      const token = await currentUser.getIdToken(true);
      const response = await fetch('http://127.0.0.1:8000/assessments', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ assessment_type: "general_test" })
      });

      if (!response.ok) {
        const errorData = await response.json();
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
      console.log("Starting new assessment");
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