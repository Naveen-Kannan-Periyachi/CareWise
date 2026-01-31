import React from 'react';
import { Target, Database, Activity } from 'lucide-react';
import './ExecutionPlan.css';

function ExecutionPlan({ plan }) {
  const getIntentColor = (intent) => {
    const colors = {
      'LITERATURE_REVIEW': '#3b82f6',
      'CLINICAL_TRIALS': '#10b981',
      'DRUG_SAFETY': '#f59e0b',
      'COMPARATIVE_RESEARCH': '#8b5cf6',
      'DATA_ANALYSIS': '#ec4899',
      'INFORMATIONAL': '#3b82f6',
      'SYMPTOMS_RELATED': '#10b981',
      'GENERAL_HEALTH': '#8b5cf6'
    };
    return colors[intent] || '#6b7280';
  };

  const getSourceBadgeColor = (source) => {
    const colors = {
      'PubMed': '#3b82f6',
      'ClinicalTrials': '#10b981',
      'FDA': '#f59e0b',
      'MedlinePlus': '#3b82f6',
      'CDC': '#10b981',
      'WHO': '#8b5cf6'
    };
    return colors[source] || '#6b7280';
  };

  return (
    <div className="execution-plan">
      <h2 className="section-title">
        <Activity size={20} />
        Execution Plan
      </h2>
      
      <div className="plan-grid">
        <div className="plan-item">
          <div className="plan-label">
            <Target size={16} />
            Intent
          </div>
          <div 
            className="plan-value intent-badge"
            style={{ backgroundColor: getIntentColor(plan.intent) }}
          >
            {plan.intent.replace(/_/g, ' ')}
          </div>
        </div>

        <div className="plan-item">
          <div className="plan-label">
            <Database size={16} />
            Data Sources
          </div>
          <div className="sources-list">
            {plan.sources.map((source, index) => (
              <span 
                key={index} 
                className="source-badge"
                style={{ backgroundColor: getSourceBadgeColor(source) }}
              >
                {source}
              </span>
            ))}
          </div>
        </div>

        <div className="plan-item entities-item">
          <div className="plan-label">Extracted Entities</div>
          <div className="entities-grid">
            {plan.entities.diseases?.length > 0 && (
              <div className="entity-group">
                <span className="entity-type">Diseases:</span>
                <div className="entity-tags">
                  {plan.entities.diseases.map((disease, idx) => (
                    <span key={idx} className="entity-tag disease-tag">
                      {disease}
                    </span>
                  ))}
                </div>
              </div>
            )}
            
            {plan.entities.drugs?.length > 0 && (
              <div className="entity-group">
                <span className="entity-type">Drugs:</span>
                <div className="entity-tags">
                  {plan.entities.drugs.map((drug, idx) => (
                    <span key={idx} className="entity-tag drug-tag">
                      {drug}
                    </span>
                  ))}
                </div>
              </div>
            )}
            
            {plan.entities.therapies?.length > 0 && (
              <div className="entity-group">
                <span className="entity-type">Therapies:</span>
                <div className="entity-tags">
                  {plan.entities.therapies.map((therapy, idx) => (
                    <span key={idx} className="entity-tag therapy-tag">
                      {therapy}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ExecutionPlan;
