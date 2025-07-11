import React, { useState } from 'react';
import styles from './FaqPage.module.css';

// Backend'den gelene kadar kullanacağımız sahte SSS verileri
const faqData = [
  {
    id: 1,
    question: 'What is the purpose of this health assistant?',
    answer: 'This AI-powered health assistant is designed for preliminary risk assessment of various cancer types based on user-provided symptoms and medical images. It is an informational tool and not a substitute for professional medical advice.'
  },
  {
    id: 2,
    question: 'Is my personal data secure?',
    answer: 'Yes, data privacy and security are our top priorities. Your personal data is only used for analysis and is processed in accordance with strict privacy principles. We do not share your data with external systems.'
  },
  {
    id: 3,
    question: 'Can I use the results as a medical diagnosis?',
    answer: 'No. The results on this website are not a medical diagnosis. The system is for informational and pre-assessment purposes only. Please consult a doctor for any health-related questions and for an actual diagnosis.'
  },
  {
    id: 4,
    question: 'How does the risk calculation work?',
    answer: 'The system uses a combination of a Large Language Model (LLM) to analyze symptoms from natural language, Machine Learning (ML) models to calculate risk scores based on questionnaire data, and Computer Vision (CV) models for image analysis. These results are combined to produce a comprehensive risk overview.'
  }
];

function FaqPage() {
  const [openId, setOpenId] = useState(null);

  const handleToggle = (id) => {
    setOpenId(openId === id ? null : id);
  };

  return (
    <div className={styles.faqContainer}>
      <h2 className={styles.title}>Frequently Asked Questions (FAQ)</h2>
      
      <div className={styles.accordion}>
        {faqData.map(item => (
          <div key={item.id} className={styles.accordionItem}>
            <button className={styles.question} onClick={() => handleToggle(item.id)}>
              {item.question}
              <span className={`${styles.icon} ${openId === item.id ? styles.open : ''}`}>+</span>
            </button>
            <div className={`${styles.answer} ${openId === item.id ? styles.open : ''}`}>
              <p>{item.answer}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default FaqPage;