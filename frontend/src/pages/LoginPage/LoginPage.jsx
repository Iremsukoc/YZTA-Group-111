import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import styles from './LoginPage.module.css';
import loginImage from '../../assets/login-page-image.png';
import eyeIcon from '../../assets/eye-icon.svg';
import googleIcon from '../../assets/google-icon.svg';


function LoginPage() {
  const [passwordVisible, setPasswordVisible] = useState(false);

  const handleLogin = (e) => {
    e.preventDefault();
    // Burada gerçek bir API çağrısı yapılabilir.
    alert('Login functionality would be implemented here!');
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
          <form onSubmit={handleLogin}>
            <div className={styles.formGroup}>
              <label className={styles.formLabel}>Email</label>
              <input type="email" className={styles.formInput} placeholder="Enter your email" required />
            </div>
            <div className={styles.formGroup}>
              <label className={styles.formLabel}>Password</label>
              <div className={styles.passwordWrapper}>
                <input type={passwordVisible ? 'text' : 'password'} className={styles.formInput} placeholder="Enter your password" required />
                <button type="button" className={styles.passwordToggle} onClick={() => setPasswordVisible(!passwordVisible)}>
                  <img src={eyeIcon} alt="Toggle Password" />
                </button>
              </div>
            </div>
            <button type="submit" className={styles.btnPrimary}>Sign In</button>
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