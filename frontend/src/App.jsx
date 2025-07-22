import React from 'react';
import { Routes, Route } from 'react-router-dom';

import Layout from './components/Layout/Layout';
import ProtectedRoute from './components/ProtectedRoute';

import HomePage from './pages/HomePage/HomePage'; 
import LoginPage from './pages/LoginPage/LoginPage';
import SignUpPage from './pages/SignUpPage/SignUpPage';
import DashboardPage from './pages/Dashboard/DashboardPage';
import MyReportsPage from './pages/MyReports/MyReportsPage';
import ProfilePage from './pages/Profile/ProfilePage';
import PasswordPage from './pages/Profile/PasswordPage';
import PersonalDetails from './pages/Profile/PersonalDetails';
import FaqPage from './pages/FaqPage/FaqPage';
import AssessmentPage from './pages/Assessment/AssessmentPage';

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/signup" element={<SignUpPage />} />

      <Route 
        element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }
      >
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/my-reports" element={<MyReportsPage />} />
        <Route path="/profile" element={<ProfilePage />}>
          <Route index element={<PersonalDetails />} />
          <Route path="password" element={<PasswordPage />} />
        </Route>
        <Route path="/faq" element={<FaqPage />} />
        <Route path="/assessment/:assessmentId" element={<AssessmentPage />} />
      </Route>

      <Route path="*" element={<div>404 - Page Not Found</div>} />
    </Routes>
  );
}

export default App;
