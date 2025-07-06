import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import styles from './SignUpPage.module.css';
import eyeIcon from '../../assets/eye-icon.svg';
import googleIcon from '../../assets/google-icon.svg';


function SignUpPage() {
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [passwordVisible, setPasswordVisible] = useState(false);
  const [confirmPasswordVisible, setConfirmPasswordVisible] = useState(false);
  const [termsAccepted, setTermsAccepted] = useState(false);
  const [passwordStrength, setPasswordStrength] = useState({ score: 0, text: 'Password strength' });
  const [isButtonDisabled, setIsButtonDisabled] = useState(true);

  useEffect(() => {
    const score = checkPasswordStrength(password);
    const text = score <= 2 ? 'Weak' : score <= 3 ? 'Medium' : 'Strong';
    if (password.length === 0) {
        setPasswordStrength({ score: 0, text: 'Password strength' });
    } else {
        setPasswordStrength({ score, text });
    }
  }, [password]);

  useEffect(() => {
    const passwordsMatch = password === confirmPassword && password.length > 0;
    const isStrongEnough = checkPasswordStrength(password) >= 2;
    setIsButtonDisabled(!(passwordsMatch && isStrongEnough && termsAccepted));
  }, [password, confirmPassword, termsAccepted]);


  const checkPasswordStrength = (pass) => {
    let score = 0;
    if (pass.length >= 8) score++;
    if (/[a-z]/.test(pass) && /[A-Z]/.test(pass)) score++;
    if (/[0-9]/.test(pass)) score++;
    if (/[^A-Za-z0-9]/.test(pass)) score++;
    return score;
  };

  const handleSignup = (e) => {
    e.preventDefault();
    if (isButtonDisabled) return;
    alert('Account creation functionality would be implemented here!');
  };

  const getStrengthBarClass = (level) => {
    if (passwordStrength.score === 0) return styles.strengthBar;
    if (passwordStrength.score <= 2) return `${styles.strengthBar} ${styles.weak}`;
    if (passwordStrength.score <= 3) return `${styles.strengthBar} ${styles.medium}`;
    return `${styles.strengthBar} ${styles.strong}`;
  };

  return (
    <div className={styles.pageContainer}>
      <div className={styles.signupContainer}>
        <div className={styles.logo}>HEALTH</div>
        <form onSubmit={handleSignup}>
          <div className={styles.formGroup}>
            <label className={styles.formLabel}>First Name</label>
            <input type="text" className={styles.formInput} placeholder="Enter your first name" required />
          </div>
          <div className={styles.formGroup}>
            <label className={styles.formLabel}>Last Name</label>
            <input type="text" className={styles.formInput} placeholder="Enter your last name" required />
          </div>
          <div className={styles.formGroup}>
            <label className={styles.formLabel}>Email Address</label>
            <input type="email" className={styles.formInput} placeholder="Enter your email address" required />
          </div>
          <div className={styles.formGroup}>
            <label className={styles.formLabel}>Password</label>
            <div className={styles.passwordWrapper}>
              <input type={passwordVisible ? 'text' : 'password'} className={styles.formInput} placeholder="Enter your password" value={password} onChange={(e) => setPassword(e.target.value)} required />
              <button type="button" className={styles.passwordToggle} onClick={() => setPasswordVisible(!passwordVisible)}>
                <img src={eyeIcon} alt="Toggle Password" />
              </button>
            </div>
            <div className={styles.passwordStrength}>
                <div className={styles.strengthIndicator}>
                    {[...Array(4)].map((_, i) => (
                        <div key={i} className={i < passwordStrength.score ? getStrengthBarClass(i + 1) : styles.strengthBar}></div>
                    ))}
                </div>
                <span>{passwordStrength.text}</span>
            </div>
          </div>
          <div className={styles.formGroup}>
            <label className={styles.formLabel}>Confirm Password</label>
            <div className={styles.passwordWrapper}>
              <input type={confirmPasswordVisible ? 'text' : 'password'} className={styles.formInput} placeholder="Confirm your password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required />
              <button type="button" className={styles.passwordToggle} onClick={() => setConfirmPasswordVisible(!confirmPasswordVisible)}>
                <img src={eyeIcon} alt="Toggle Password" />
              </button>
            </div>
          </div>
          <div className={styles.checkboxGroup}>
            <div className={`${styles.checkbox} ${termsAccepted ? styles.checked : ''}`} onClick={() => setTermsAccepted(!termsAccepted)}>
              {termsAccepted && '✓'}
            </div>
            <label className={styles.checkboxLabel}>I agree to the <Link to="/terms">Terms & Conditions</Link></label>
          </div>
          <button type="submit" className={styles.btnPrimary} disabled={isButtonDisabled}>Create an account</button>
          <button type="button" className={styles.btnGoogle}>
            <img src={googleIcon} alt="Google Icon" className={styles.googleIcon} />
            Sign In with Google
          </button>        
        </form>
        <div className={styles.switchLink}>
          Have an account? <Link to="/login">Sign In</Link>
        </div>
      </div>
    </div>
  );
}

export default SignUpPage;