import React, { useState } from 'react';
import { FileText, ChevronDown, ChevronUp } from 'lucide-react';
import EvidenceCard from './EvidenceCard';
import './EvidenceList.css';

function EvidenceList({ evidence }) {
  const [showAll, setShowAll] = useState(false);
  const displayCount = showAll ? evidence.length : 5;

  return (
    <div className="evidence-list">
      <h2 className="section-title">
        <FileText size={20} />
        Evidence Items ({evidence.length})
      </h2>

      <div className="evidence-grid">
        {evidence.slice(0, displayCount).map((item, index) => (
          <EvidenceCard key={index} evidence={item} rank={index + 1} />
        ))}
      </div>

      {evidence.length > 5 && (
        <div className="show-more-container">
          <button 
            className="show-more-button"
            onClick={() => setShowAll(!showAll)}
          >
            {showAll ? (
              <>
                <ChevronUp size={20} />
                Show Less
              </>
            ) : (
              <>
                <ChevronDown size={20} />
                Show {evidence.length - 5} More Evidence Items
              </>
            )}
          </button>
        </div>
      )}
    </div>
  );
}

export default EvidenceList;
