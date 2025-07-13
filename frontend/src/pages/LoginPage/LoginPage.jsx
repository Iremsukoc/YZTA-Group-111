import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import styles from './LoginPage.module.css';
import loginImage from '../../assets/login-page-image.png';
import eyeIcon from '../../assets/eye-icon.svg';
import googleIcon from '../../assets/google-icon.svg';

function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const [passwordVisible, setPasswordVisible] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      setError('');
      setLoading(true);
      await login(email, password);
      navigate("/dashboard");
    } catch (err) {
      console.error("Firebase'den gelen GERÇEK login hatası:", err.code, err.message);
      
      setError("Login failed. Please check your e-mail and password.");
    }
    setLoading(false);
  };

  return (
    <div className={styles.pageContainer}>
      <div className={styles.loginContainer}>
        <div className={styles.leftSide}>
          <img src={loginImage} alt="Illustration" />
        </div>
        <div className={styles.rightSide}>
          <div className={styles.logo}>HEALTH</div>
          <h1 className={styles.welcomeTitle}>Welcome Back</h1>
          <p className={styles.welcomeSubtitle}>Enter your email and password to access your account</p>
          
          {error && <div className={styles.errorMessage}>{error}</div>}

          <form onSubmit={handleLogin}>
            <div className={styles.formGroup}>
              <label className={styles.formLabel}>Email</label>
              <input type="email" className={styles.formInput} placeholder="Enter your email" required value={email} onChange={(e) => setEmail(e.target.value)} />
            </div>
            <div className={styles.formGroup}>
              <label className={styles.formLabel}>Password</label>
              <div className={styles.passwordWrapper}>
                <input 
                  type={passwordVisible ? 'text' : 'password'} 
                  className={styles.formInput} 
                  placeholder="Enter your password" 
                  required 
                  value={password} 
                  onChange={(e) => setPassword(e.target.value)} 
                />
                <button type="button" className={styles.passwordToggle} onClick={() => setPasswordVisible(!passwordVisible)}>
                  <img src={eyeIcon} alt="Toggle Password" />
                </button>
              </div>
            </div>
            <button type="submit" disabled={loading} className={styles.btnPrimary}>
              {loading ? 'Logging in...' : 'Sign In'}
            </button>
            <button type="button" className={styles.btnGoogle}>
              <img src={googleIcon} alt="Google Icon" className={styles.googleIcon} />
              Sign In with Google
            </button>
          </form>
          <div className={styles.switchLink}>
            Don't have an account? <Link to="/signup">Sign Up</Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;