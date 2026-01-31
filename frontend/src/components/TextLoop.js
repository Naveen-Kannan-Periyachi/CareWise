import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const TextLoop = ({ items, interval = 2000, className = '' }) => {
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentIndex((current) => (current + 1) % items.length);
    }, interval);
    
    return () => clearInterval(timer);
  }, [items.length, interval]);

  const motionVariants = {
    initial: { y: 20, opacity: 0 },
    animate: { y: 0, opacity: 1 },
    exit: { y: -20, opacity: 0 },
  };

  return (
    <div className={`text-loop-container ${className}`}>
      <AnimatePresence mode="wait">
        <motion.div
          key={currentIndex}
          initial="initial"
          animate="animate"
          exit="exit"
          transition={{ duration: 0.3 }}
          variants={motionVariants}
        >
          {items[currentIndex]}
        </motion.div>
      </AnimatePresence>
    </div>
  );
};

export default TextLoop;
