import React, { useState, useEffect, useRef, useMemo } from 'react';
import { useParams } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import styles from './AssessmentPage.module.css';
import Message from '../../components/Chat/Message';
import ChatInput from '../../components/Chat/ChatInput';
import NotificationToast from '../../components/NotificationToast/NotificationToast'; 
import { doc, getDoc } from 'firebase/firestore';
import { db } from '../../firebase.js';
import { fetchAssessmentDetail } from '../../api/AssessmentApi';

const ChatWelcomeScreen = ({ name }) => (
  <div className={styles.welcomeContainer}>
    <h2 className={styles.welcomeTitle}>Welcome {name}</h2>
  </div>
);

function AssessmentPage() {
  const { assessmentId } = useParams();
  const { currentUser } = useAuth();
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [assessmentStatus, setAssessmentStatus] = useState(null); 
  const [userData, setUserData] = useState(null);
  const [popup, setPopup] = useState({ show: false, message: '', type: '' }); 
  const [assessmentDetail, setAssessmentDetail] = useState(null);
  const messageListRef = useRef(null);


  useEffect(() => {
    const fetchUserData = async () => {
      if (currentUser) {
        try {
          const userDocRef = doc(db, 'users', currentUser.uid);
          const userDoc = await getDoc(userDocRef);
          if (userDoc.exists()) {
            setUserData(userDoc.data());
          }
        } catch (err) {
          console.error("Failed to fetch user data:", err);
        }
      }
    };
    fetchUserData();
  }, [currentUser]);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const data = await fetchAssessmentDetail(assessmentId);
        const conv = data.conversation || [];
        
        // If assessment is completed but no diagnosis message exists, create one
        if (data.status === 'completed' && (data.risk_level || data.confidence != null)) {
          const hasDiagnosis = conv.some(m => m.type === 'diagnosis');
          if (!hasDiagnosis) {
            conv.push({
              role: 'assistant',
              type: 'diagnosis',
              content: {
                title: "Diagnosis Complete",
                result: data.risk_level,
                confidence: data.confidence,
                note: "Note: This is not a final diagnosis. Please consult a medical professional."
              }
            });
          }
        }
        
        setMessages(conv);
        setAssessmentStatus(data.status);
        setAssessmentDetail(data);
      } catch (err) {
        console.error("Assessment detayları alınamadı:", err);
      }
    };
    if (currentUser && assessmentId) {
      fetchHistory();
    }
  }, [assessmentId, currentUser]);

  useEffect(() => {
    if (messageListRef.current) {
      messageListRef.current.scrollTop = messageListRef.current.scrollHeight;
    }
  }, [messages]);

  useEffect(() => {
    if (assessmentDetail?.status) {
      setAssessmentStatus(assessmentDetail.status);
    }
  }, [assessmentDetail?.status]);
  
  const stageLabel = useMemo(() => {
    switch (assessmentStatus) {
      case "general_test_in_progress":
        return "🩺 Stage 1: General Health Assessment";
      case "triage_in_progress":
        return "🔍 Stage 2: Triage Assessment";
      case "detailed_qa_in_progress":
        return "📋 Stage 3: Detailed Analysis";
      case "awaiting_image":
        return "📷 Stage 4: Image Upload and Analysis";
      case "completed":
        return "✅ Assessment Completed";
      default:
        return "";
    }
  }, [assessmentStatus]);
  
  const handleSendMessage = async (userMessage) => {
    if (!assessmentId) return;
  
    const userMsgObject = { role: 'user', content: userMessage };
    setMessages(prev => [...prev, userMsgObject]);
    setIsLoading(true);
  
    try {
      const token = await currentUser.getIdToken();
      const response = await fetch(`http://127.0.0.1:8000/assessments/${assessmentId}/messages`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ content: userMessage })
      });
  
      const responseData = await response.json();
      if (!response.ok) throw new Error(responseData.detail || "Failed to get response.");
  
      const assistantMsgObject = { role: 'assistant', content: responseData.content };
      setMessages(prev => [...prev, assistantMsgObject]);
  
      if (responseData.new_status) {
        setAssessmentStatus(responseData.new_status);
      }
  
    } catch (err) {
      console.error("Message error:", err);
      setMessages(prev => [...prev, { role: 'assistant', content: 'LLM hatası oluştu.' }]);
    } finally {
      setIsLoading(false);
    }
  };
  

  const handleImageSelected = async (file) => {
    setIsLoading(true);
    setPopup({ show: true, message: 'Görüntü yükleniyor ve analiz ediliyor...', type: 'success' });

    const formData = new FormData();
    formData.append('image_file', file);
    const mdl =
      (assessmentDetail?.suspectedCancerType && ['brain','skin','breast'].includes(assessmentDetail.suspectedCancerType))
        ? assessmentDetail.suspectedCancerType
        : (assessmentDetail?.assessment_type && ['brain','skin','breast'].includes(assessmentDetail.assessment_type))
        ? assessmentDetail.assessment_type
        : 'brain';

    formData.append('model_type', mdl);
    try {
      const token = await currentUser.getIdToken();
      const response = await fetch(`http://127.0.0.1:8000/assessments/${assessmentId}/image`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData,
      });
      const result = await response.json();
      if (!response.ok) throw new Error(result.detail || 'Görüntü analizi başarısız oldu.');

      setPopup({ show: true, message: 'Görüntü başarıyla analiz edildi!', type: 'success' });

      // Refresh the assessment data to get the updated conversation with diagnosis message
      const updatedData = await fetchAssessmentDetail(assessmentId);
      setMessages(updatedData.conversation || []);
      setAssessmentStatus('completed');

    } catch (error) {
      setPopup({ show: true, message: error.message, type: 'error' });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.pageContainer}>
      {popup.show && (
        <NotificationToast
          message={popup.message}
          type={popup.type}
          onClose={() => setPopup({ show: false, message: '', type: '' })}
        />
      )}

      <div className={styles.phaseInfo}>
        {assessmentStatus === "general_test_in_progress" && "🩺 Stage 1: General Health Assessment"}
        {assessmentStatus === "triage_in_progress" && "🔍 Stage 2: Triage Assessment"}
        {assessmentStatus === "detailed_qa_in_progress" && "📋 Stage 3: Detailed Analysis"}
        {assessmentStatus === "awaiting_image" && "📷 Stage 4: Image Upload and Analysis"}
        {assessmentStatus === "completed" && "✅ Assessment Completed"}
      </div>

      <div className={styles.chatContainer}>
        <div className={styles.chatWrapper}>

          <div className={styles.messageList} ref={messageListRef}>
            {messages.length === 0 && !isLoading ? (
              <ChatWelcomeScreen name={userData?.first_name || 'User'} />
            ) : (
              messages.map((msg, index) => (
                <Message key={index} message={msg} />
              ))
            )}

            {isLoading && (
              <div className={styles.loadingIndicator}>
                Assistant is typing...
              </div>
            )}
          </div>

          {assessmentStatus === 'completed' && (
            <div className={styles.assessmentComplete}>
              The assessment is complete. Thank you.
            </div>
          )}

          {assessmentStatus !== 'completed' && (
            <ChatInput
              onSendMessage={handleSendMessage}
              isLoading={isLoading}
              isImageUploadAllowed={assessmentStatus === "awaiting_image"}
              onImageSelected={handleImageSelected}
            />
          )}
        </div>
      </div>
    </div>
  );
}

export default AssessmentPage;
