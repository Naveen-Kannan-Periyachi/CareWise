import React from 'react';
import { Link } from 'react-router-dom';
import { Heart, Microscope, Database, Sparkles, ChevronRight, Shield, Zap, Users } from 'lucide-react';
import FlowFieldBackground from '../components/FlowFieldBackground';
import './LandingPage.css';

const LandingPage = () => {
  return (
    <div className="landing-page">
      <FlowFieldBackground color="#818cf8" trailOpacity={0.1} particleCount={1000} speed={0.8} />
      {/* Navbar */}
      <nav className="navbar">
        <div className="nav-container">
          <div className="nav-logo">
            <Heart className="logo-icon" />
            <span className="logo-text">CareWise</span>
          </div>
          <div className="nav-links">
            <Link to="/login" className="nav-link">Login</Link>
            <Link to="/signup" className="nav-button">Get Started</Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-container">
          <div className="hero-content fade-in">
            <div className="hero-badge">
              <Sparkles size={16} />
              <span>AI-Powered Health Research</span>
            </div>
            <h1 className="hero-title">
              Your Unified <span className="gradient-text">Health Research</span> Assistant
            </h1>
            <p className="hero-description">
              Get instant access to biomedical research and trusted health information from 6 authoritative sources. 
              CareWise combines PubMed, FDA, ClinicalTrials, MedlinePlus, CDC, and WHO in one intelligent platform.
            </p>
            <div className="hero-buttons">
              <Link to="/signup" className="primary-button">
                Start Researching
                <ChevronRight size={20} />
              </Link>
              <Link to="/login" className="secondary-button">
                Login
              </Link>
            </div>
            <div className="hero-stats">
              <div className="stat">
                <div className="stat-number">6</div>
                <div className="stat-label">Data Sources</div>
              </div>
              <div className="stat">
                <div className="stat-number">8</div>
                <div className="stat-label">Query Types</div>
              </div>
              <div className="stat">
                <div className="stat-number">∞</div>
                <div className="stat-label">Possibilities</div>
              </div>
            </div>
          </div>
          <div className="hero-visual">
            <div className="floating-card card-1">
              <Microscope size={32} />
              <div className="card-text">
                <h4>Biomedical Research</h4>
                <p>Latest studies & trials</p>
              </div>
            </div>
            <div className="floating-card card-2">
              <Heart size={32} />
              <div className="card-text">
                <h4>General Health</h4>
                <p>Trusted medical info</p>
              </div>
            </div>
            <div className="floating-card card-3">
              <Database size={32} />
              <div className="card-text">
                <h4>Real-Time Data</h4>
                <p>Live API connections</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <div className="features-container">
          <div className="section-header">
            <h2>Powerful Features</h2>
            <p>Everything you need for comprehensive health research</p>
          </div>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon" style={{background: 'var(--gradient-1)'}}>
                <Zap size={24} />
              </div>
              <h3>Instant Answers</h3>
              <p>Get grounded, evidence-based answers powered by advanced AI and real medical data.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon" style={{background: 'var(--gradient-2)'}}>
                <Database size={24} />
              </div>
              <h3>6 Trusted Sources</h3>
              <p>Access PubMed, FDA, ClinicalTrials, MedlinePlus, CDC, and WHO simultaneously.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon" style={{background: 'var(--gradient-3)'}}>
                <Shield size={24} />
              </div>
              <h3>Verified Information</h3>
              <p>All information comes from authoritative medical and scientific databases.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon" style={{background: 'var(--gradient-1)'}}>
                <Microscope size={24} />
              </div>
              <h3>Smart Routing</h3>
              <p>Automatically routes queries to the most relevant data sources.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon" style={{background: 'var(--gradient-2)'}}>
                <Heart size={24} />
              </div>
              <h3>Dual Mode</h3>
              <p>Supports both biomedical research and general health information queries.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon" style={{background: 'var(--gradient-3)'}}>
                <Users size={24} />
              </div>
              <h3>Chat History</h3>
              <p>Save and revisit your research conversations anytime.</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="cta-container">
          <h2>Ready to start your health research?</h2>
          <p>Join CareWise today and get instant access to comprehensive health information.</p>
          <Link to="/signup" className="cta-button">
            Get Started Free
            <ChevronRight size={20} />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <div className="footer-content">
          <div className="footer-brand">
            <Heart className="footer-logo" />
            <span>CareWise</span>
          </div>
          <p className="footer-text">
            Unified Health Research Assistant • Version 2.0
          </p>
          <p className="footer-sources">
            Powered by: PubMed • ClinicalTrials.gov • FDA • MedlinePlus • CDC • WHO
          </p>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
