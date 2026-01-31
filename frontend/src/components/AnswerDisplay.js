import React from 'react';
import { MessageSquare, ExternalLink } from 'lucide-react';
import './AnswerDisplay.css';

function AnswerDisplay({ answer }) {
  const formatAnswerWithCitations = (text) => {
    // Replace source citations with styled badges
    const parts = text.split(/(\[PubMed\]|\[ClinicalTrials\]|\[FDA\]|\[MedlinePlus\]|\[CDC\]|\[WHO\])/g);
    
    return parts.map((part, index) => {
      if (part === '[PubMed]') {
        return <span key={index} className="citation-badge pubmed-badge">PubMed</span>;
      } else if (part === '[ClinicalTrials]') {
        return <span key={index} className="citation-badge trials-badge">ClinicalTrials</span>;
      } else if (part === '[FDA]') {
        return <span key={index} className="citation-badge fda-badge">FDA</span>;
      } else if (part === '[MedlinePlus]') {
        return <span key={index} className="citation-badge pubmed-badge">MedlinePlus</span>;
      } else if (part === '[CDC]') {
        return <span key={index} className="citation-badge trials-badge">CDC</span>;
      } else if (part === '[WHO]') {
        return <span key={index} className="citation-badge fda-badge">WHO</span>;
      }
      return <span key={index}>{part}</span>;
    });
  };

  return (
    <div className="answer-display">
      <h2 className="section-title">
        <MessageSquare size={20} />
        AI-Generated Answer
      </h2>
      
      <div className="answer-content">
        <div className="answer-text">
          {formatAnswerWithCitations(answer.answer)}
        </div>
        
        {answer.sources_used && answer.sources_used.length > 0 && (
          <div className="sources-section">
            <h3 className="sources-title">
              <ExternalLink size={16} />
              Sources Cited ({answer.sources_used.length})
            </h3>
            <div className="sources-list">
              {answer.sources_used.map((source, index) => (
                <div key={index} className="source-item">
                  <span className="source-number">[{index + 1}]</span>
                  <div className="source-details">
                    <span className="source-name">{source.source}</span>
                    <span className="source-title">{source.title}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
        
        <div className="answer-footer">
          <span className="evidence-count">
            Based on {answer.evidence_count} evidence item{answer.evidence_count !== 1 ? 's' : ''}
          </span>
        </div>
      </div>
    </div>
  );
}

export default AnswerDisplay;
