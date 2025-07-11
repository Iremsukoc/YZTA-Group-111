import React from 'react';
import { useAuth } from '../../context/AuthContext';
import styles from './MyReportsPage.module.css';
import ReportCard from '../../components/ReportCard/ReportCard';

import { Doughnut } from 'react-chartjs-2';
import { Chart, ArcElement, Tooltip, Legend } from 'chart.js';
Chart.register(ArcElement, Tooltip, Legend);

// Backend'den gelene kadar kullanacağımız sahte veriler
const mockReports = [
  { id: 1, title: 'Lung Cancer Analysis', date: 'July 8, 2025', riskLevel: 'High' },
  { id: 2, title: 'Brain Tumor Detection', date: 'June 25, 2025', riskLevel: 'Low' },
  { id: 3, title: 'General Symptom Check', date: 'May 12, 2025', riskLevel: 'Medium' },
];

const chartData = {
  datasets: [
    {
      data: [65, 35],
      backgroundColor: ['#4A90E2', '#E9ECEF'],
      borderColor: ['#ffffff'],
      borderWidth: 4,
      borderRadius: 10,
      cutout: '75%',
    },
  ],
};

const chartOptions = {
  plugins: {
    legend: { display: false },
    tooltip: { enabled: false },
  },
  maintainAspectRatio: false,
};

function MyReportsPage() {
  const { currentUser } = useAuth();
  const firstName = currentUser?.reloadUserInfo?.customAttributes ? JSON.parse(currentUser.reloadUserInfo.customAttributes).firstName : 'User';

  return (
    <div className={styles.dashboardPage}>
      <header className={styles.header}>
        <div className={styles.welcomeMessage}>
          <h2>Welcome back, {firstName}!</h2>
          <p>Here is your health overview and recent reports.</p>
        </div>
        <button className={styles.newAssessmentBtn}>
          Start New Assessment
        </button>
      </header>

      <div className={styles.mainContent}>
        <section className={styles.reportsSection}>
          <div className={styles.sectionHeader}>
            <h3>Recent Reports</h3>
            <a href="#" className={styles.seeAllLink}>See All</a>
          </div>
          <div className={styles.reportsList}>
            {mockReports.map(report => (
              <ReportCard key={report.id} report={report} />
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