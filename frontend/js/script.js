// Password toggle functionality
document.addEventListener('DOMContentLoaded', () => {
    const toggleButtons = document.querySelectorAll('.password-toggle');
    toggleButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const input = btn.previousElementSibling;
        input.type = input.type === 'password' ? 'text' : 'password';
      });
    });
  
    // Form submission example
    const form = document.querySelector('form');
    if (form) {
      form.addEventListener('submit', (e) => {
        e.preventDefault();
        alert('Login functionality would be implemented here!');
      });
    }
  });

  document.addEventListener('DOMContentLoaded', () => {
    // Password toggle for all password-toggle buttons
    document.querySelectorAll('.password-toggle').forEach(btn => {
      btn.addEventListener('click', () => {
        const input = btn.previousElementSibling;
        input.type = input.type === 'password' ? 'text' : 'password';
      });
    });
  
    // Signup-specific logic
    let termsAccepted = false;
    const termsCheckbox = document.getElementById('termsCheckbox');
    const createBtn = document.getElementById('createAccountBtn');
  
    if (termsCheckbox && createBtn) {
      termsCheckbox.addEventListener('click', () => {
        termsAccepted = !termsAccepted;
        termsCheckbox.style.background = termsAccepted ? '#4A90E2' : 'white';
        termsCheckbox.style.border = '2px solid #4A90E2';
        updateCreateButton();
      });
    }
  
    function updateCreateButton() {
      const password = document.getElementById('password').value;
      const confirmPassword = document.getElementById('confirmPassword').value;
      const passwordsMatch = password === confirmPassword && password.length > 0;
      const passwordStrong = password.length >= 8;
      if (termsAccepted && passwordsMatch && passwordStrong) {
        createBtn.disabled = false;
      } else {
        createBtn.disabled = true;
      }
    }
  
    const passwordInput = document.getElementById('password');
    if (passwordInput) {
      passwordInput.addEventListener('input', () => {
        const password = passwordInput.value;
        const strengthBars = document.querySelectorAll('.strength-bar');
        const strengthText = document.getElementById('strength-text');
        let strength = 0;
        if (password.length >= 8) strength++;
        if (/[a-z]/.test(password)) strength++;
        if (/[A-Z]/.test(password)) strength++;
        if (/[0-9]/.test(password)) strength++;
        if (/[^A-Za-z0-9]/.test(password)) strength++;
  
        strengthBars.forEach(bar => bar.className = 'strength-bar');
  
        if (strength <= 2) {
          strengthText.textContent = 'Weak';
          for (let i = 0; i < Math.min(strength, 2); i++) strengthBars[i].classList.add('active', 'weak');
        } else if (strength <= 3) {
          strengthText.textContent = 'Medium';
          for (let i = 0; i < 3; i++) strengthBars[i].classList.add('active', 'medium');
        } else {
          strengthText.textContent = 'Strong';
          for (let i = 0; i < 4; i++) strengthBars[i].classList.add('active', 'strong');
        }
        updateCreateButton();
      });
    }
  
    const confirmPasswordInput = document.getElementById('confirmPassword');
    if (confirmPasswordInput) {
      confirmPasswordInput.addEventListener('input', () => updateCreateButton());
    }
  
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
      signupForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        if (password !== confirmPassword) {
          alert('Passwords do not match!');
          return;
        }
        if (!termsAccepted) {
          alert('Please accept the Terms & Conditions!');
          return;
        }
        alert('Account creation functionality would be implemented here!');
      });
    }
  });
  
  