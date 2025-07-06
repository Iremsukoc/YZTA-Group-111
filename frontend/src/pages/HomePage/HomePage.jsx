import React from 'react';
import Header from '../../components/Header/header';
import FeatureCard from '../../components/FeatureCard/FeatureCard';
import styles from './HomePage.module.css';

// İmajları import ediyoruz
import clipboardIcon from '../../assets/clipboard.svg';
import chartIcon from '../../assets/chart.svg';
import imageIcon from '../../assets/image.svg';

const featuresData = [
  {
    icon: clipboardIcon,
    title: 'General Test',
    description: 'Complete the questionnaire to assess your susceptibility to various cancers.',
  },
  {
    icon: chartIcon,
    title: 'Risk Calculation',
    description: 'An ML model estimates your chances of developing cancer',
  },
  {
    icon: imageIcon,
    title: 'Image Analysis',
    description: 'Upload medical images for detection through image processing',
  },
];

function HomePage() {
  return (
    <div className={styles.homePage}>
      <Header />
      <main className={styles.mainContent}>
        <h1 className={styles.mainTitle}>Cancer Risk Assessment</h1>
        <p className={styles.mainDescription}>
          Determine your potential risk of developing different types of cancer with our three-step process.
        </p>
        <div className={styles.features}>
          {featuresData.map((feature, index) => (
            <FeatureCard
              key={index}
              icon={feature.icon}
              title={feature.title}
              description={feature.description}
            />
          ))}
        </div>
        <div className={styles.disclaimer}>
          The results on this website are not a medical diagnosis. Please consult a doctor for any health-related questions.
        </div>
      </main>
    </div>
  );
}

export default HomePage;