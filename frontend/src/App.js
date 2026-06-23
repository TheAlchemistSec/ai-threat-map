import React, { useState } from 'react';
import './App.css';

function App() {
  const [appName, setAppName] = useState('');
  const [llmType, setLlmType] = useState('Claude');
  const [features, setFeatures] = useState('');
  const [dataTypes, setDataTypes] = useState('');
  const [loading, setLoading] = useState(false);
  const [threatModel, setThreatModel] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/threat-model?app_name=' + appName + '&llm_type=' + llmType + '&features=' + features + '&data_types=' + dataTypes, {
        method: 'POST'
      });
      const data = await response.json();
      setThreatModel(data);
    } catch (error) {
      console.error('Error:', error);
      alert('Error generating threat model');
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <h1>AI Threat Map</h1>
       {threatModel && threatModel.risk_level && (
  <div className={`risk-summary risk-${threatModel.risk_level.toLowerCase()}`}>
    <div className="risk-score">
      <h3>Overall Risk Score: {threatModel.risk_score}%</h3>
      <p className="risk-level">Risk Level: <strong>{threatModel.risk_level}</strong></p>
    </div>
    <div className="threat-stats">
      <span className="stat high">🔴 High: {threatModel.threat_breakdown.high}</span>
      <span className="stat medium">🟡 Medium: {threatModel.threat_breakdown.medium}</span>
      <span className="stat low">🟢 Low: {threatModel.threat_breakdown.low}</span>
    </div>
  </div>
)}
      <p>LLM Threat Modeling Tool</p>
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>App Name</label>
          <input value={appName} onChange={(e) => setAppName(e.target.value)} placeholder="e.g., Customer Support Chatbot" required />
        </div>
        
        <div className="form-group">
          <label>LLM Type</label>
          <select value={llmType} onChange={(e) => setLlmType(e.target.value)}>
            <option>Claude</option>
            <option>GPT-4</option>
            <option>Other</option>
          </select>
        </div>
        
        <div className="form-group">
          <label>Features</label>
          <textarea value={features} onChange={(e) => setFeatures(e.target.value)} placeholder="e.g., file uploads, web search, integrations" required />
        </div>
        
        <div className="form-group">
          <label>Data Types Processed</label>
          <textarea value={dataTypes} onChange={(e) => setDataTypes(e.target.value)} placeholder="e.g., customer emails, financial records" required />
        </div>
        
        <button type="submit" disabled={loading}>
          {loading ? 'Generating...' : 'Generate Threat Model'}
        </button>
      </form>

      {threatModel && threatModel.threat_model && (
        <div className="result">
          <h2>Threat Model Report</h2>
          <div className="threats-container">
            {threatModel.threat_model.split('\n').map((line, idx) => {
              if (line.trim() && line.includes('|')) {
                let severity = 'low';
                if (line.toUpperCase().includes('HIGH')) {
                  severity = 'high';
                } else if (line.toUpperCase().includes('MEDIUM')) {
                  severity = 'medium';
                }
                return (
                  <div key={idx} className={`threat ${severity}`}>
                    {line}
                  </div>
                );
              }
              return null;
            })}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;