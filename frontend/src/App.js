import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './styles.css';

// Create axios instance with base URL
const api = axios.create({
  baseURL: process.env.NODE_ENV === 'production' 
    ? '/api' 
    : 'http://localhost:5000/api'
});

function App() {
  const [cvs, setCvs] = useState([]);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    experience: '',
    education: ''
  });
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchCVs();
  }, []);

  const fetchCVs = async () => {
    try {
        console.log('Fetching CVs...');  // Debug log
        const response = await api.get('/cvs');
        console.log('Response:', response.data);  // Debug log
        setCvs(response.data);
        setError(null);
    } catch (err) {
        console.error('Error details:', err.response || err);  // More detailed error logging
        setError(`Failed to fetch CVs: ${err.message}`);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/cvs', formData);
      fetchCVs();
      setFormData({ name: '', email: '', experience: '', education: '' });
      setError(null);
    } catch (err) {
      console.error('Error creating CV:', err);
      setError('Failed to create CV');
    }
  };

  const handleDownload = async () => {
    try {
      const response = await api.get('/download', {
        responseType: 'blob'
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'system_control.zip');
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      setError(null);
    } catch (err) {
      console.error('Error downloading file:', err);
      setError('Failed to download file');
    }
  };

  return (
    <div className="container">
      <header className="header">
        <h1>CV Creator</h1>
      </header>
      
      {error && <div className="error-message">{error}</div>}
      
      <div className="form-container">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="name">Name</label>
            <input
              id="name"
              type="text"
              className="form-control"
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              className="form-control"
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="experience">Experience</label>
            <textarea
              id="experience"
              className="form-control"
              value={formData.experience}
              onChange={(e) => setFormData({...formData, experience: e.target.value})}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="education">Education</label>
            <textarea
              id="education"
              className="form-control"
              value={formData.education}
              onChange={(e) => setFormData({...formData, education: e.target.value})}
            />
          </div>
          
          <button type="submit" className="btn btn-primary">Create CV</button>
        </form>
      </div>
      
      <button onClick={handleDownload} className="btn btn-secondary">
        Download System Control App
      </button>
      
      <div className="cv-list">
        {cvs.map(cv => (
          <div key={cv.id} className="cv-card">
            <h3>{cv.name}</h3>
            <p><strong>Email:</strong> {cv.email}</p>
            <p><strong>Experience:</strong> {cv.experience}</p>
            <p><strong>Education:</strong> {cv.education}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
