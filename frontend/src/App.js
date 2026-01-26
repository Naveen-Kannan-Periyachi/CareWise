import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import QueryInput from './components/QueryInput';
import ExecutionPlan from './components/ExecutionPlan';
import AnswerDisplay from './components/AnswerDisplay';
import EvidenceList from './components/EvidenceList';
import LoadingSpinner from './components/LoadingSpinner';
import { Dna } from 'lucide-react';

function App() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [results, setResults] = useState(null);

  const handleSearch = async (searchQuery) => {
    setLoading(true);
    setError(null);
    setResults(null);
    setQuery(searchQuery);

    try {
      const response = await axios.post('/api/query', {
        query: searchQuery
      });
      
      setResults(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred while processing your query. Please try again.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <div className="header-content">
          <div className="logo">
            <Dna size={40} className="dna-icon" />
            <h1>CareWise Bio</h1>
          </div>
          <p className="tagline">AI-Powered Biomedical Research Assistant</p>
        </div>
      </header>

      <main className="App-main">
        <div className="container">
          <QueryInput onSearch={handleSearch} loading={loading} />

          {error && (
            <div className="error-message">
              <p>⚠️ {error}</p>
            </div>
          )}

          {loading && <LoadingSpinner />}

          {results && !loading && (
            <div className="results-container">
              {results.execution_plan && (
                <ExecutionPlan plan={results.execution_plan} />
              )}

              {results.answer && (
                <AnswerDisplay answer={results.answer} />
              )}

              {results.evidence && results.evidence.length > 0 && (
                <EvidenceList evidence={results.evidence} />
              )}

              {results.evidence && results.evidence.length === 0 && (
                <div className="no-results">
                  <p>No evidence found for your query. Try rephrasing or using different keywords.</p>
                </div>
              )}
            </div>
          )}
        </div>
      </main>

      <footer className="App-footer">
        <p>Powered by Ollama LLM • PubMed • ClinicalTrials.gov • FDA</p>
      </footer>
    </div>
  );
}

export default App;
