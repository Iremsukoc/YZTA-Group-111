import React, { useEffect, useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { doc, getDoc } from 'firebase/firestore';
import { db } from '../../firebase.js';
import styles from './MyReportsPage.module.css';
import ReportCard from '../../components/ReportCard/ReportCard';
import { fetchReportSummaries, startNewAssessment } from '../../api/AssessmentApi';
import { useNavigate } from 'react-router-dom';

import { Doughnut } from 'react-chartjs-2';
import { Chart, ArcElement, Tooltip, Legend } from 'chart.js';
Chart.register(ArcElement, Tooltip, Legend);

function MyReportsPage() {
  const { currentUser } = useAuth();
  const [reports, setReports] = useState([]);
  const [userData, setUserData] = useState(null);
  const navigate = useNavigate();

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

  const firstName = userData?.first_name || (currentUser?.reloadUserInfo?.customAttributes
    ? JSON.parse(currentUser.reloadUserInfo.customAttributes).firstName
    : 'User');

  useEffect(() => {
    const loadReports = async () => {
      try {
        const data = await fetchReportSummaries();
        setReports(data);
      } catch (error) {
        console.error("Raporlar alınamadı:", error);
      }
    };
    loadReports();
  }, []);

  const handleStartAssessment = async () => {
    try {
      const data = await startNewAssessment();
      navigate(`/assessment/${data.assessment_id}`);
    } catch (error) {
      console.error("Assessment başlatma hatası:", error);
    }
  };

  const riskCounts = reports.reduce(
    (acc, report) => {
      const level = report.risk_level;
      if (level === 'High Risk') acc.high++;
      else if (level === 'Moderate Risk') acc.medium++;
      else if (level === 'Low Risk') acc.low++;
      else if (level === 'No Risk') acc.none++;
      return acc;
    },
    { high: 0, medium: 0, low: 0, none: 0 }
  );

  const chartData = {
    datasets: [
      {
        data: [riskCounts.high, riskCounts.medium, riskCounts.low, riskCounts.none],
        backgroundColor: ['#E63946', '#F4A261', '#2A9D8F', '#BDBDBD'],
        borderColor: ['#ffffff'],
        borderWidth: 4,
        borderRadius: 10,
        cutout: '75%',
      },
    ],
    labels: ['High Risk', 'Moderate Risk', 'Low Risk', 'No Risk'],
  };

  const chartOptions = {
    plugins: {
      legend: { display: false },
      tooltip: { enabled: true },
    },
    maintainAspectRatio: false,
  };

  return (
    <div className={styles.dashboardPage}>
      <header className={styles.header}>
        <div className={styles.welcomeMessage}>
          <h2>Hello, {firstName}</h2>
          <p>Here is your health overview and recent reports.</p>
        </div>
        <button className={styles.newAssessmentBtn} onClick={handleStartAssessment}>
          Start New Assessment
        </button>
      </header>

      <div className={styles.mainContent}>
        <section className={styles.reportsSection}>
          <div className={styles.sectionHeader}>
            <h3>Recent Reports</h3>
          </div>
          <div className={styles.reportsList}>
            {reports.map((report) => (
              <ReportCard
                key={report.assessment_id}
                report={{
                  id: report.assessment_id,
                  title: report.title || report.assessmentName || report.assessment_name || report.assessment_type,
                  date: new Date(report.created_at).toLocaleDateString(),
                  riskLevel: report.risk_level || 'Unknown',
                  status: report.status,
                  canContinue: report.can_continue,
                  confidence: report.confidence,  
                }}
                onClick={() => navigate(`/assessment/${report.assessment_id}`)}

              />
            ))}
          </div>
        </section>

        <aside className={styles.riskOverview}>
          <h3>Risk Overview</h3>
          <div className={styles.chartContainer}>
            <Doughnut data={chartData} options={chartOptions} />
          </div>
          <p>Your overall risk score is calculated based on your latest reports.</p>
        </aside>
      </div>
    </div>
  );
}



export default MyReportsPage;
