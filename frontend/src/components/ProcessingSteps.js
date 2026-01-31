import React from 'react';
import { motion } from 'framer-motion';
import { Loader2, Brain, Database, Search, FileText } from 'lucide-react';
import './ProcessingSteps.css';

const ProcessingSteps = ({ currentStatus = 'analyzing' }) => {
  console.log('ProcessingSteps rendering with status:', currentStatus);
  
  // Map status to display info
  const statusMap = {
    'analyzing': { icon: <Brain size={18} />, title: 'Analyzing your question' },
    'plan_complete': { icon: <Brain size={18} />, title: 'Analysis complete' },
    'selecting_sources': { icon: <Database size={18} />, title: 'Selecting data sources' },
    'searching': { icon: <Search size={18} />, title: 'Searching databases' },
    'generating': { icon: <FileText size={18} />, title: 'Generating answer' }
  };

  const currentStep = statusMap[currentStatus] || statusMap['analyzing'];

  return (
    <div className="processing-steps-compact">
      <motion.div 
        className="processing-spinner"
        animate={{ rotate: 360 }}
        transition={{ 
          duration: 1,
          repeat: Infinity,
          ease: "linear"
        }}
      >
        <Loader2 size={20} />
      </motion.div>
      <div className="processing-text">
        <motion.div 
          className="processing-step-item"
          key={currentStatus}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          <span className="step-icon-inline">{currentStep.icon}</span>
          <span>{currentStep.title}</span>
        </motion.div>
      </div>
    </div>
  );
};

export default ProcessingSteps;

