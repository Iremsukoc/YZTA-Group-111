import React, { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import styles from './AssessmentPage.module.css';
import Message from '../../components/Chat/Message';
import ChatInput from '../../components/Chat/ChatInput';
import logoRegAI from '../../assets/logo-regai.png';


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
  const messageListRef = useRef(null);
  const firstName = currentUser?.reloadUserInfo?.customAttributes 
                  ? JSON.parse(currentUser.reloadUserInfo.customAttributes).firstName 
                  : 'User';


  useEffect(() => {
    // Gerçekte burada backend'den /assessments/:id endpoint'i ile geçmiş çekilecek.
  }, [assessmentId, currentUser]);

  useEffect(() => {
    if (messageListRef.current) {
      messageListRef.current.scrollTop = messageListRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSendMessage = async (userMessage) => {
    if (!assessmentId) return;

    const newMessages = messages.length === 0 
      ? [{ role: 'assistant', content: 'Hello! How can I help you with your health concerns today?' }, { role: 'user', content: userMessage }]
      : [...messages, { role: 'user', content: userMessage }];

    setMessages(newMessages);
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

      if (!response.ok) throw new Error("Failed to get response from backend.");

      const data = await response.json();
      setMessages(prev => [...prev, data]);
    } catch (error) {
      console.error("Failed to send message:", error);
      setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, there was an error processing your message.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.pageContainer}>
      <div className={styles.chatContainer}>
        
        <div className={styles.chatWrapper}>
          
          <div className={styles.messageList} ref={messageListRef}>
            {messages.length === 0 ? (
              <ChatWelcomeScreen name={firstName} />
            ) : (
              messages.map((msg, index) => <Message key={index} message={msg} />)
            )}
            {isLoading && <div className={styles.loadingIndicator}>Assistant is typing...</div>}
          </div>

          <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
          
        </div>
        
      </div>
    </div>
  );
}

export default AssessmentPage;