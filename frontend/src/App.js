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
      setThreatModel(data.threat_model);
    } catch (error) {
      console.error('Error:', error);
      alert('Error generating threat model');
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <h1>AI ThreadMap</h1>
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

      {threatModel && (
        <div className="results">
          <h2>Threat Model Report</h2>
          <pre>{threatModel}</pre>
        </div>
      )}
    </div>
  );
}

export default App;