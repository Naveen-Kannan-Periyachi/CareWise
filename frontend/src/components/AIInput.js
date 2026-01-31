import React, { useState, useEffect } from "react";
import { CornerRightUp } from "lucide-react";
import { useAutoResizeTextarea } from "../hooks/useAutoResizeTextarea";
import "./AIInput.css";

export function AIInput({
  id = "ai-input",
  placeholder = "Ask me anything about health...",
  minHeight = 56,
  maxHeight = 200,
  loadingDuration = 3000,
  onSubmit,
  className = "",
  disabled = false
}) {
  const [inputValue, setInputValue] = useState("");
  const [submitted, setSubmitted] = useState(false);
  
  const { textareaRef, adjustHeight } = useAutoResizeTextarea({
    minHeight,
    maxHeight,
  });

  const handleSubmit = async () => {
    if (!inputValue.trim() || submitted || disabled) return;
    
    setSubmitted(true);
    if (onSubmit) {
      await onSubmit(inputValue);
    }
    setInputValue("");
    adjustHeight(true);
    
    setTimeout(() => {
      setSubmitted(false);
    }, loadingDuration);
  };

  return (
    <div className={`ai-input-container ${className}`}>
      <div className="ai-input-wrapper">
        <div className="ai-input-field-wrapper">
          <textarea
            id={id}
            placeholder={placeholder}
            className="ai-input-field"
            ref={textareaRef}
            value={inputValue}
            onChange={(e) => {
              setInputValue(e.target.value);
              adjustHeight();
            }}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSubmit();
              }
            }}
            disabled={submitted || disabled}
            rows={1}
          />
          <button
            onClick={handleSubmit}
            className={`ai-input-submit ${submitted ? 'ai-input-submit-loading' : ''}`}
            type="button"
            disabled={submitted || disabled || !inputValue.trim()}
          >
            {submitted ? (
              <div className="ai-input-spinner" />
            ) : (
              <CornerRightUp
                className={`ai-input-icon ${inputValue ? 'ai-input-icon-active' : ''}`}
                size={18}
              />
            )}
          </button>
        </div>
        <p className="ai-input-status">
          {submitted ? "AI is thinking..." : "Press Enter to send"}
        </p>
      </div>
    </div>
  );
}

export default AIInput;
