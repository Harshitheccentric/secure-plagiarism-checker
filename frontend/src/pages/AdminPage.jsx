import React, { useState } from 'react';
import FileList from '../components/FileList';
import ReportTable from '../components/ReportTable';
import apiService from '../apiService';
import React, { useState, useEffect } from 'react';
import { getEncryptedFiles, decryptFile, generateReport } from '../apiService';
import ReportDisplay from '../components/ReportDisplay';

const AdminPage = () => {
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [systemStatus, setSystemStatus] = useState(null);
  const [cleanupStatus, setCleanupStatus] = useState(null);
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [reportData, setReportData] = useState(null);
  const [reportLoading, setReportLoading] = useState(false);
  const [selectedMethod, setSelectedMethod] = useState('word_based');

  const handleDecryptFile = () => {
    // Trigger refresh when a file is decrypted
    setRefreshTrigger(prev => prev + 1);
  };

  const handleCleanup = async () => {
    try {
      setCleanupStatus({ type: 'loading', message: 'Cleaning up temporary files...' });
      const response = await apiService.cleanup();
      
      setCleanupStatus({
        type: 'success',
        message: response.data.message
      });
      
      // Auto-clear status after 3 seconds
      setTimeout(() => setCleanupStatus(null), 3000);
      
    } catch (error) {
      setCleanupStatus({
        type: 'error',
        message: error.response?.data?.error || 'Cleanup failed'
      });
    }
  };

  

  const checkSystemHealth = async () => {
    try {
      setSystemStatus({ type: 'loading', message: 'Checking system health...' });
      const response = await apiService.healthCheck();
      
      setSystemStatus({
        type: 'success',
        message: `System is healthy. ${response.data.message}`
      });
      
      // Auto-clear status after 3 seconds
      setTimeout(() => setSystemStatus(null), 3000);
      
    } catch (error) {
      setSystemStatus({
        type: 'error',
        message: 'System health check failed'
      });
    }
  };

  return (
    <div className="container">
      <div className="card text-center">
        <h1> Administrator Dashboard</h1>
        <p className="text-muted">
          Manage encrypted submissions and generate plagiarism detection reports
        </p>
        
        <div className="d-flex justify-center gap-2 mt-3">
          <button 
            className="btn btn-secondary btn-small"
            onClick={checkSystemHealth}
          >
             System Health
          </button>
          <button 
            className="btn btn-warning btn-small"
            onClick={handleCleanup}
          >
             Cleanup Temp Files
          </button>
        </div>
        
        {systemStatus && (
          <div className={`mt-2 ${systemStatus.type}`}>
            {systemStatus.type === 'loading' && <div className="loading-spinner" style={{ display: 'inline-block', marginRight: '0.5rem' }}></div>}
            {systemStatus.message}
          </div>
        )}
        
        {cleanupStatus && (
          <div className={`mt-2 ${cleanupStatus.type}`}>
            {cleanupStatus.type === 'loading' && <div className="loading-spinner" style={{ display: 'inline-block', marginRight: '0.5rem' }}></div>}
            {cleanupStatus.message}
          </div>
        )}
      </div>

      <FileList 
        refreshTrigger={refreshTrigger}
        onDecryptFile={handleDecryptFile}
      />

      <ReportTable refreshTrigger={refreshTrigger} />

      <div className="card">
        <h3> How to Use the Admin Dashboard</h3>
        <div style={{ background: '#f8f9ff', padding: '1.5rem', borderRadius: '8px', marginTop: '1rem' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem' }}>
            <div>
              <h4> File Management</h4>
              <ul style={{ marginLeft: '1rem', lineHeight: '1.6' }}>
                <li>View all encrypted student submissions</li>
                <li>Decrypt and download individual files for review</li>
                <li>Monitor file upload timestamps and sizes</li>
              </ul>
            </div>
            
            <div>
              <h4> Plagiarism Detection</h4>
              <ul style={{ marginLeft: '1rem', lineHeight: '1.6' }}>
                <li>Choose detection method (word/character/line-based)</li>
                <li>Generate comprehensive similarity reports</li>
                <li>Download reports as JSON files</li>
                <li>View detailed comparison statistics</li>
              </ul>
            </div>
            
            <div>
              <h4> System Maintenance</h4>
              <ul style={{ marginLeft: '1rem', lineHeight: '1.6' }}>
                <li>Check API health and connectivity</li>
                <li>Clean up temporary decrypted files</li>
                <li>Monitor system performance</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <div className="card">
        <h3> Similarity Thresholds</h3>
        <div style={{ background: '#f0f8ff', padding: '1.5rem', borderRadius: '8px', marginTop: '1rem' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
            <div>
              <span className="status-badge status-high">🚨 HIGH (≥80%)</span>
              <p className="text-small mt-1">Likely plagiarism - requires investigation</p>
            </div>
            <div>
              <span className="status-badge status-medium">⚠️ MEDIUM (50-79%)</span>
              <p className="text-small mt-1">Suspicious similarities - review recommended</p>
            </div>
            <div>
              <span className="status-badge status-low">ℹ️ LOW (20-49%)</span>
              <p className="text-small mt-1">Some overlap - may be acceptable</p>
            </div>
            <div>
              <span className="status-badge status-minimal">✅ MINIMAL (&lt;20%)</span>
              <p className="text-small mt-1">Minimal similarity - likely original work</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminPage;
