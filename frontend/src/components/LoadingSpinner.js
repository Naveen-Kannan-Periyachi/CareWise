import React from 'react';
import { Loader2 } from 'lucide-react';
import './LoadingSpinner.css';

function LoadingSpinner() {
  return (
    <div className="loading-container">
      <div className="loading-spinner">
        <Loader2 size={48} className="spinner-icon" />
        <h3>Searching biomedical databases...</h3>
        <div className="loading-steps">
          <div className="loading-step">
            <div className="step-dot active"></div>
            <span>Planning query with LLM</span>
          </div>
          <div className="loading-step">
            <div className="step-dot active"></div>
            <span>Fetching from PubMed, ClinicalTrials, FDA</span>
          </div>
          <div className="loading-step">
            <div className="step-dot active"></div>
            <span>Ranking evidence by relevance</span>
          </div>
          <div className="loading-step">
            <div className="step-dot active"></div>
            <span>Generating grounded answer</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LoadingSpinner;
