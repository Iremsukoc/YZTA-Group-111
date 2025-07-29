const API_BASE_URL = "http://127.0.0.1:8000";

import { getAuth } from 'firebase/auth';

async function getAuthToken() {
  const auth = getAuth();
  const currentUser = auth.currentUser;
  if (!currentUser) throw new Error("Kullanıcı oturumu yok.");
  return await currentUser.getIdToken();
}

export async function fetchAssessments(token) {
  const res = await fetch(`${API_BASE_URL}/assessments`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });

  if (!res.ok) throw new Error('Failed to fetch assessments');
  return res.json();
}

export async function fetchReportSummaries() {
  const token = await getAuthToken();
  const response = await fetch(`${API_BASE_URL}/assessments/report_summaries`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });

  if (!response.ok) {
    throw new Error("Sunucudan raporlar alınamadı");
  }
  const data = await response.json();
  return data;
}

export async function startNewAssessment(assessmentType = 'general_test') {
    const token = await getAuthToken();
    const response = await fetch('http://127.0.0.1:8000/assessments', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
        assessment_type: assessmentType
      })
    });
  
    if (!response.ok) {
      throw new Error('Assessment başlatılamadı');
    }
  
    return await response.json();
  }

  export async function fetchAssessmentDetail(assessmentId) {
    const token = await getAuthToken();
    const res = await fetch(`http://127.0.0.1:8000/assessments/${assessmentId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  
    if (!res.ok) {
      throw new Error("Failed to fetch assessment detail");
    }
  
    return await res.json();
  }
  
  
