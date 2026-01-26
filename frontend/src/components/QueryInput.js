import React, { useState } from 'react';
import { Search, Sparkles } from 'lucide-react';
import './QueryInput.css';

const EXAMPLE_QUERIES = [
  "Any ongoing CAR-T trials for melanoma?",
  "What are the side effects of Pembrolizumab?",
  "Latest research on CRISPR gene therapy for sickle cell disease",
  "Clinical trials for Alzheimer's disease treatment",
  "Compare chemotherapy and immunotherapy for lung cancer"
];

function QueryInput({ onSearch, loading }) {
  const [inputValue, setInputValue] = useState('');
  const [showExamples, setShowExamples] = useState(true);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputValue.trim() && !loading) {
      onSearch(inputValue.trim());
      setShowExamples(false);
    }
  };

  const handleExampleClick = (example) => {
    setInputValue(example);
    onSearch(example);
    setShowExamples(false);
  };

  return (
    <div className="query-input-container">
      <form onSubmit={handleSubmit} className="search-form">
        <div className="search-input-wrapper">
          <Search className="search-icon" size={24} />
          <input
            type="text"
            className="search-input"
            placeholder="Ask a biomedical research question..."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            disabled={loading}
          />
          <button 
            type="submit" 
            className="search-button"
            disabled={loading || !inputValue.trim()}
          >
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>
      </form>

      {showExamples && (
        <div className="examples-section">
          <div className="examples-header">
            <Sparkles size={18} />
            <span>Try these examples:</span>
          </div>
          <div className="examples-grid">
            {EXAMPLE_QUERIES.map((example, index) => (
              <button
                key={index}
                className="example-button"
                onClick={() => handleExampleClick(example)}
                disabled={loading}
              >
                {example}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default QueryInput;
