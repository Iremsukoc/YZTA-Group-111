import React, { useState } from 'react';
import styles from './FaqPage.module.css';

// Backend'den gelene kadar kullanacağımız sahte SSS verileri
const faqData = [
  {
    id: 1,
    question: 'What is the purpose of this health assistant?',
    answer: 'regAI is designed to assist users in evaluating potential cancer risks through a combination of AI-powered conversations and medical image analysis. It is not a substitute for professional medical advice but serves as an early awareness and guidance tool.'
  },
  {
    id: 2,
    question: 'How does the risk calculation work?',
    answer: 'No. regAI is not a certified diagnostic tool. The results should not be interpreted as a definitive medical diagnosis. Always consult with a qualified healthcare provider for clinical assessment and treatment.'
  },
  {
    id: 3,
    question: 'Can I use the results as a medical diagnosis?',
    answer: 'No. The results on this website are not a medical diagnosis. The system is for informational and pre-assessment purposes only. Please consult a doctor for any health-related questions and for an actual diagnosis.'
  },
  {
    id: 4,
    question: 'What types of medical images are supported??',
    answer: 'You can upload common imaging formats such as CT, MRI, X-ray, and PET/CT scans. These are processed by our AI model to detect signs of cancer or abnormal tissue patterns.'
  },
  {
    id: 5,
    question: 'Is my personal data secure?',
    answer: 'Yes. We adhere to international data protection standards. All personal data and medical images are encrypted and used strictly for AI analysis within the application. No data is shared with third parties.'
  },
  {
    id: 6,
    question: 'What happens to my images after analysis?',
    answer: 'Uploaded images are processed and then securely stored only if you give permission. Otherwise, they are automatically deleted after analysis is complete.'
  },
  {
    id: 7,
    question: 'Can the AI assistant understand complex or vague symptoms?',
    answer: 'Yes. Our LLM (Gemini 2.5 Pro) is capable of interpreting natural language and follows up with more specific questions to guide you through a medically relevant assessment path.'
  },
  {
    id: 8,
    question: 'Will I be contacted by a real doctor?',
    answer: 'Not directly through regAI. However, if your risk level is high, the system can guide you toward scheduling an appointment with the appropriate specialist.'
  },
  {
    id: 9,
    question: 'Which cancers does the system cover?',
    answer: 'Currently, regAI focuses on the early detection of common cancers such as lung, brain, breast, skin, colon and leukemia cancer. Support for more types is being added over time.'
  },
  
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