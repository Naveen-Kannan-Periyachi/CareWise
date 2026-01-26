import React, { useState } from 'react';
import { ChevronDown, ChevronUp, Award, Calendar, Database } from 'lucide-react';
import './EvidenceCard.css';

function EvidenceCard({ evidence, rank }) {
  const [expanded, setExpanded] = useState(false);

  const getSourceColor = (source) => {
    const colors = {
      'PubMed': '#3b82f6',
      'ClinicalTrials': '#10b981',
      'FDA': '#f59e0b'
    };
    return colors[source] || '#6b7280';
  };

  const getScoreColor = (score) => {
    if (score >= 0.8) return '#10b981';
    if (score >= 0.6) return '#f59e0b';
    return '#6b7280';
  };

  const truncateText = (text, maxLength) => {
    if (!text) return 'No content available';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  };

  return (
    <div className="evidence-card">
      <div className="card-header">
        <div className="rank-badge" style={{ backgroundColor: rank <= 3 ? '#fbbf24' : '#94a3b8' }}>
          #{rank}
        </div>
        <div 
          className="source-badge-large"
          style={{ backgroundColor: getSourceColor(evidence.source) }}
        >
          <Database size={14} />
          {evidence.source}
        </div>
        <div 
          className="score-badge"
          style={{ color: getScoreColor(evidence.score) }}
        >
          <Award size={14} />
          {(evidence.score * 100).toFixed(0)}%
        </div>
      </div>

      <h3 className="evidence-title">{evidence.title}</h3>

      <div className="evidence-content">
        <p className="content-text">
          {expanded 
            ? evidence.content 
            : truncateText(evidence.content, 250)
          }
        </p>
      </div>

      {evidence.metadata && (
        <div className="metadata-section">
          {evidence.metadata.year && (
            <div className="metadata-item">
              <Calendar size={14} />
              <span>{evidence.metadata.year}</span>
            </div>
          )}
          {evidence.metadata.type && (
            <div className="metadata-item">
              <span className="metadata-type">{evidence.metadata.type.replace(/_/g, ' ')}</span>
            </div>
          )}
          {evidence.metadata.status && (
            <div className="metadata-item">
              <span className="status-badge">{evidence.metadata.status}</span>
            </div>
          )}
          {evidence.metadata.phase && (
            <div className="metadata-item">
              <span className="phase-badge">{evidence.metadata.phase}</span>
            </div>
          )}
        </div>
      )}

      {evidence.scores_breakdown && expanded && (
        <div className="scores-breakdown">
          <h4 className="breakdown-title">Relevance Breakdown:</h4>
          <div className="breakdown-grid">
            {Object.entries(evidence.scores_breakdown).map(([key, value]) => (
              <div key={key} className="breakdown-item">
                <span className="breakdown-label">
                  {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}:
                </span>
                <div className="breakdown-bar">
                  <div 
                    className="breakdown-fill"
                    style={{ 
                      width: `${value * 100}%`,
                      backgroundColor: getScoreColor(value)
                    }}
                  />
                </div>
                <span className="breakdown-value">{(value * 100).toFixed(0)}%</span>
              </div>
            ))}
          </div>
        </div>
      )}

      <button 
        className="expand-button"
        onClick={() => setExpanded(!expanded)}
      >
        {expanded ? (
          <>
            <ChevronUp size={16} />
            Show Less
          </>
        ) : (
          <>
            <ChevronDown size={16} />
            Show More
          </>
        )}
      </button>
    </div>
  );
}

export default EvidenceCard;
