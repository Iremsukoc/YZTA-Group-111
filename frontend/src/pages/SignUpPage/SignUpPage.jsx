import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import styles from './SignUpPage.module.css';
import eyeIcon from '../../assets/eye-icon.svg';
import googleIcon from '../../assets/google-icon.svg';


function SignUpPage() {
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    
    const [passwordVisible, setPasswordVisible] = useState(false);
    const [confirmPasswordVisible, setConfirmPasswordVisible] = useState(false);
    
    const [strength, setStrength] = useState({ score: 0, text: '' });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        if (password.length === 0) {
            setStrength({ score: 0, text: '' });
            return;
        }
        let score = 0;
        if (/.{8,}/.test(password)) score++;
        if (/[a-z]/.test(password) && /[A-Z]/.test(password)) score++;
        if (/[0-9]/.test(password)) score++;
        if (/[^A-Za-z0-9]/.test(password)) score++;
        let text = 'Weak';
        if (score > 1) text = 'Medium';
        if (score > 2) text = 'Strong';
        setStrength({ score, text });
    }, [password]);

    const handleSignup = async (e) => {
        e.preventDefault();
        setError('');

        if (!firstName || !lastName || !email || !password || !confirmPassword) {
            return setError("All fields are required.");
        }
        
        if (password !== confirmPassword) {
            return setError("Passwords do not match!");
        }
        if (strength.score < 2) {
            return setError("Please choose a stronger password.");
        }

        setLoading(true);
        try {
            const response = await fetch('http://127.0.0.1:8000/api/v1/auth/signup', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    first_name: firstName,
                    last_name: lastName,
                    email: email,
                    password: password
                }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                
                if (errorData.detail && Array.isArray(errorData.detail)) {
                    const firstError = errorData.detail[0];
                    const readableMessage = `Invalid value for ${firstError.loc[1]}: ${firstError.msg}`;
                    throw new Error(readableMessage); 
                
                } else if (errorData.detail) {
                    throw new Error(errorData.detail);
                } else {
                    throw new Error('An unexpected error occurred.');
                }
            }
            
            alert('Your account has been created successfully! You can now log in.');
            navigate('/login');

        } catch (err) {
            setError(err.message); 
            console.error("Signup error:", err);
        }
        setLoading(false);
        };
    
    const getStrengthBarClass = () => {
        if (strength.score <= 1) return styles.weak;
        if (strength.score <= 2) return styles.medium;
        return styles.strong;
    };

    return (
        <div className={styles.pageContainer}>
            <div className={styles.signupContainer}>
                <div className={styles.logo}>HEALTH</div>
                
                {error && <div className={styles.errorMessage}>{error}</div>}

                <form id="signupForm" onSubmit={handleSignup} noValidate>
                    <div className={styles.formGroup}>
                        <label className={styles.formLabel}>First Name</label>
                        <input type="text" className={styles.formInput} placeholder="Enter your first name" value={firstName} onChange={(e) => setFirstName(e.target.value)} />
                    </div>
                    <div className={styles.formGroup}>
                        <label className={styles.formLabel}>Last Name</label>
                        <input type="text" className={styles.formInput} placeholder="Enter your last name" value={lastName} onChange={(e) => setLastName(e.target.value)} />
                    </div>
                    <div className={styles.formGroup}>
                        <label className={styles.formLabel}>Email Address</label>
                        <input type="email" className={styles.formInput} placeholder="Enter your email address" value={email} onChange={(e) => setEmail(e.target.value)} />
                    </div>
                    <div className={styles.formGroup}>
                        <label className={styles.formLabel}>Password</label>
                        <div className={styles.passwordWrapper}>
                            <input type={passwordVisible ? 'text' : 'password'} className={styles.formInput} placeholder="Enter your password" value={password} onChange={(e) => setPassword(e.target.value)} />
                            <button type="button" className={styles.passwordToggle} onClick={() => setPasswordVisible(!passwordVisible)}><img src={eyeIcon} alt="Show Password" /></button>
                        </div>
                        <div className={styles.passwordStrength}>
                            <div className={styles.strengthIndicator}>
                                {[...Array(4)].map((_, i) => (
                                    <div key={i} className={`${styles.strengthBar} ${i < strength.score ? getStrengthBarClass() : ''}`}></div>
                                ))}
                            </div>
                            <span>{strength.text}</span>
                        </div>
                    </div>
                    <div className={styles.formGroup}>
                        <label className={styles.formLabel}>Confirm Password</label>
                        <div className={styles.passwordWrapper}>
                            <input type={confirmPasswordVisible ? 'text' : 'password'} className={styles.formInput} placeholder="Confirm your password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} />
                            <button type="button" className={styles.passwordToggle} onClick={() => setConfirmPasswordVisible(!confirmPasswordVisible)}><img src={eyeIcon} alt="Show Password" /></button>
                        </div>
                    </div>
                    
                    <button type="submit" disabled={loading} className={styles.btnPrimary}>
                        {loading ? 'Creating Account...' : 'Create an account'}
                    </button>
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