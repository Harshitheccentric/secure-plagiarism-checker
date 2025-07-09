import React, { useState } from 'react';
import apiService from '../apiService';

const ReportTable = ({ refreshTrigger }) => {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [method, setMethod] = useState('word_based');

  const generateReport = async () => {
    try {
      setLoading(true);
      setError(null);
      setReport(null);
      
      const response = await apiService.generateReport(method);
      setReport(response.data);
      
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to generate report');
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status) => {
    const statusClass = `status-badge status-${status.toLowerCase()}`;
    const statusEmoji = {
      'HIGH': '🚨',
      'MEDIUM': '⚠️',
      'LOW': 'ℹ️',
      'MINIMAL': '✅'
    };
    
    return (
      <span className={statusClass}>
        {statusEmoji[status]} {status}
      </span>
    );
  };

  const downloadReport = async () => {
    if (!report || !report.report_saved) return;
    
    try {
      const response = await apiService.downloadReport(report.report_saved);
      
      // Create blob and download
      const blob = new Blob([response.data], { type: 'application/json' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = report.report_saved;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
    } catch (err) {
      setError('Failed to download report');
    }
  };

  return (
    <div className="card">
      <h2> Plagiarism Detection Report</h2>
      
      <div className="form-group">
        <label className="form-label">Detection Method:</label>
        <select 
          className="form-select"
          value={method}
          onChange={(e) => setMethod(e.target.value)}
          disabled={loading}
        >
          <option value="word_based">Word-based Analysis</option>
          <option value="char_based">Character-based Analysis</option>
          <option value="line_based">Line-based Analysis</option>
        </select>
      </div>

      <div className="d-flex gap-2 mb-3">
        <button 
          className="btn btn-primary"
          onClick={generateReport}
          disabled={loading}
        >
          {loading ? (
            <>
              <div className="loading-spinner"></div>
              Analyzing Files...
            </>
          ) : (
            <>
               Generate Report
            </>
          )}
        </button>
        
        {report && report.report_saved && (
          <button 
            className="btn btn-secondary"
            onClick={downloadReport}
          >
             Download Report
          </button>
        )}
      </div>

      {error && (
        <div className="error">
          {error}
        </div>
      )}

      {report && (
        <div>
          {/* Summary Statistics */}
          <div className="card" style={{ background: '#f8f9ff', border: '1px solid #e1e8ed' }}>
            <h3> Summary Statistics</h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
              <div>
                <div className="text-small text-muted">Total Files</div>
                <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{report.summary.total_files}</div>
              </div>
              <div>
                <div className="text-small text-muted">Comparisons Made</div>
                <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{report.summary.total_comparisons}</div>
              </div>
              <div>
                <div className="text-small text-muted">Average Similarity</div>
                <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{report.summary.average_similarity}%</div>
              </div>
              <div>
                <div className="text-small text-muted">Highest Similarity</div>
                <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: report.summary.highest_similarity >= 80 ? '#e74c3c' : '#27ae60' }}>
                  {report.summary.highest_similarity}%
                </div>
              </div>
              <div>
                <div className="text-small text-muted">Suspicious Pairs (≥50%)</div>
                <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: report.summary.suspicious_pairs > 0 ? '#f39c12' : '#27ae60' }}>
                  {report.summary.suspicious_pairs}
                </div>
              </div>
              <div>
                <div className="text-small text-muted">High Risk Pairs (≥80%)</div>
                <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: report.summary.high_risk_pairs > 0 ? '#e74c3c' : '#27ae60' }}>
                  {report.summary.high_risk_pairs}
                </div>
              </div>
            </div>
          </div>

          {/* Detailed Comparisons */}
          <h3> Detailed Comparison Results</h3>
          <div className="text-small text-muted mb-2">
            Method: {report.method} • Generated: {new Date(report.timestamp).toLocaleString()}
          </div>

          {report.comparisons && report.comparisons.length > 0 ? (
            <div className="table-container">
              <table className="table">
                <thead>
                  <tr>
                    <th>File 1</th>
                    <th>File 2</th>
                    <th>Similarity</th>
                    <th>Segments</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {report.comparisons.map((comparison, index) => (
                    <tr key={index}>
                      <td>{comparison.file1}</td>
                      <td>{comparison.file2}</td>
                      <td>
                        <strong style={{ 
                          color: comparison.similarity >= 80 ? '#e74c3c' : 
                                 comparison.similarity >= 50 ? '#f39c12' : 
                                 comparison.similarity >= 20 ? '#3498db' : '#27ae60'
                        }}>
                          {comparison.similarity}%
                        </strong>
                      </td>
                      <td>{comparison.common_segments}</td>
                      <td>{getStatusBadge(comparison.status)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="info">
              No comparisons available. Need at least 2 files to generate a report.
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ReportTable;
