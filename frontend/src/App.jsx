import React from 'react';
import { Routes, Route } from 'react-router-dom';

import Layout from './components/Layout/Layout';
import ProtectedRoute from './components/ProtectedRoute';

import LoginPage from './pages/LoginPage/LoginPage';
import SignUpPage from './pages/SignUpPage/SignUpPage';
import DashboardPage from './pages/Dashboard/DashboardPage';
import ProfilePage from './pages/Profile/ProfilePage';
import PasswordPage from './pages/Profile/PasswordPage';
import PersonalDetails from './pages/Profile/PersonalDetails';
import MyReportsPage from './pages/MyReports/MyReportsPage'; 
import FaqPage from './pages/FaqPage/FaqPage';



function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/signup" element={<SignUpPage />} />

      <Route 
        path="/" 
        element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }
      >
        <Route index element={<DashboardPage />} />
        <Route path="dashboard" element={<DashboardPage />} />
        <Route path="my-reports" element={<MyReportsPage />} /> 
        <Route path="profile" element={<ProfilePage />}>
          <Route index element={<PersonalDetails />} /> 
          <Route path="password" element={<PasswordPage />} />
        </Route>
        <Route path="faq" element={<FaqPage />} />
      </Route>

      <Route path="*" element={<div>404 - Page Not Found</div>} />
    </Routes>
  );
}

export default App;
