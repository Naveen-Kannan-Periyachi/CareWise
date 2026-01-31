import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Heart, Mail, Lock, AlertCircle } from 'lucide-react';
import BackgroundPaths from '../components/BackgroundPaths';
import './Auth.css';

const Login = ({ setIsAuthenticated }) => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    password: ''
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
    setLoading(true);

    try {
      // API call to backend
      const response = await fetch('http://localhost:8000/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: formData.email,
          password: formData.password
        })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Login failed');
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
              <h2>Welcome Back!</h2>
              <p>Access your health research dashboard</p>
            </div>
          </div>
          <div className="auth-features">
            <div className="auth-feature">
              <div className="feature-check">✓</div>
              <span>6 Medical Sources</span>
            </div>
            <div className="auth-feature">
              <div className="feature-check">✓</div>
              <span>AI-Powered</span>
            </div>
            <div className="auth-feature">
              <div className="feature-check">✓</div>
              <span>Chat History</span>
            </div>
          </div>
        </div>

        <div className="auth-form-container">
          <div className="auth-form-wrapper">
            <div className="auth-header">
              <h1>Login to CareWise</h1>
              <p>Enter your credentials to access your account</p>
            </div>

            {error && (
              <div className="auth-error">
                <AlertCircle size={20} />
                <span>{error}</span>
              </div>
            )}

            <form onSubmit={handleSubmit} className="auth-form">
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
                  />
                </div>
              </div>

              <div className="form-footer">
                <label className="checkbox-label">
                  <input type="checkbox" />
                  <span>Remember me</span>
                </label>
                <a href="#" className="forgot-link">Forgot password?</a>
              </div>

              <button type="submit" className="auth-submit-btn" disabled={loading}>
                {loading ? 'Logging in...' : 'Login'}
              </button>
            </form>

            <div className="auth-alt">
              <p>Don't have an account? <Link to="/signup">Sign up</Link></p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
