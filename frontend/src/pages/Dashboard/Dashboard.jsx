import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';

function Dashboard() {
  const { currentUser, logout } = useAuth();
  const [backendData, setBackendData] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProtectedData = async () => {
      if (!currentUser) {
        setLoading(false);
        return;
      }

      try {
        const token = await currentUser.getIdToken();

        const response = await fetch('http://127.0.0.1:8000/api/v1/users/me', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Backend request failed!');
        }

        const data = await response.json();
        setBackendData(data);

      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchProtectedData();
  }, [currentUser]);

  if (loading) {
    return <div>Loading...</div>;
  }

  // Ana JSX yapısı
  return (
    <div style={{ padding: '2rem', fontFamily: 'monospace' }}>
      <h1>Protected Dashboard Page</h1>
      <p>Bu sayfayı görebiliyorsanız, başarıyla giriş yaptınız ve korunmuş bir rotaya eriştiniz.</p>
      
      <hr />

      <p><strong>Giriş Yapan Kullanıcı (Firebase'den):</strong> {currentUser?.email}</p>
      
      <hr />

      <h2>Backend'den Gelen Veri (/users/me):</h2>
      {error && <p style={{ color: 'red' }}>HATA: {error}</p>}
      
      {backendData ? (
        <pre style={{ backgroundColor: '#f0f0f0', padding: '1rem', border: '1px solid #ccc' }}>
          {JSON.stringify(backendData, null, 2)}
        </pre>
      ) : (
        <p>Backend'den veri bekleniyor...</p>
      )}

      <br />
      <button onClick={() => logout().then(() => navigate('/login'))}>
        Log Out
      </button>
    </div>
  );
}

export default Dashboard;