import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Heart, Mail, Lock, User, AlertCircle } from 'lucide-react';
import BackgroundPaths from '../components/BackgroundPaths';
import './Auth.css';

const Signup = ({ setIsAuthenticated }) => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    // Validation
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (formData.password.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }

    setLoading(true);

    try {
      // API call to backend
      const response = await fetch('http://localhost:8000/auth/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: formData.name,
          email: formData.email,
          password: formData.password
        })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Signup failed');
      }

      const user = await response.json();

      // Save user to localStorage
      localStorage.setItem('carewise_user', JSON.stringify({
        name: user.name,
        email: user.email
      }));
      
      setIsAuthenticated(true);
      navigate('/dashboard');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <BackgroundPaths />
      <div className="auth-container">
        <div className="auth-sidebar">
          <div className="auth-sidebar-left">
            <Link to="/" className="auth-logo">
              <Heart className="logo-icon" />
              <span>CareWise</span>
            </Link>
            <div className="auth-sidebar-content">
              <h2>Start Your Research Journey</h2>
              <p>Access trusted medical information</p>
            </div>
          </div>
          <div className="auth-features">
            <div className="auth-feature">
              <div className="feature-check">✓</div>
              <span>6 Medical Databases</span>
            </div>
            <div className="auth-feature">
              <div className="feature-check">✓</div>
              <span>AI Insights</span>
            </div>
            <div className="auth-feature">
              <div className="feature-check">✓</div>
              <span>Free Forever</span>
            </div>
          </div>
        </div>

        <div className="auth-form-container">
          <div className="auth-form-wrapper">
            <div className="auth-header">
              <h1>Create Account</h1>
              <p>Get started with CareWise in seconds</p>
            </div>

            {error && (
              <div className="auth-error">
                <AlertCircle size={20} />
                <span>{error}</span>
              </div>
            )}

            <form onSubmit={handleSubmit} className="auth-form">
              <div className="form-group">
                <label htmlFor="name">Full Name</label>
                <div className="input-wrapper">
                  <User size={20} className="input-icon" />
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    placeholder="John Doe"
                    required
                  />
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="email">Email Address</label>
                <div className="input-wrapper">
                  <Mail size={20} className="input-icon" />
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="you@example.com"
                    required
                  />
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="password">Password</label>
                <div className="input-wrapper">
                  <Lock size={20} className="input-icon" />
                  <input
                    type="password"
                    id="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    placeholder="••••••••"
                    required
                    minLength="6"
                  />
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="confirmPassword">Confirm Password</label>
                <div className="input-wrapper">
                  <Lock size={20} className="input-icon" />
                  <input
                    type="password"
                    id="confirmPassword"
                    name="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    placeholder="••••••••"
                    required
                    minLength="6"
                  />
                </div>
              </div>

              <label className="checkbox-label" style={{marginBottom: '1.5rem'}}>
                <input type="checkbox" required />
                <span>I agree to the Terms of Service and Privacy Policy</span>
              </label>

              <button type="submit" className="auth-submit-btn" disabled={loading}>
                {loading ? 'Creating account...' : 'Create Account'}
              </button>
            </form>

            <div className="auth-alt">
              <p>Already have an account? <Link to="/login">Login</Link></p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Signup;
