import React, { useState, useEffect } from 'react';
import apiService from '../apiService';

const FileList = ({ refreshTrigger, onDecryptFile }) => {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [decryptingFile, setDecryptingFile] = useState(null);

  const fetchFiles = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiService.getFiles();
      setFiles(response.data.files);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch files');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFiles();
  }, [refreshTrigger]);

  const handleDecrypt = async (filename) => {
    try {
      setDecryptingFile(filename);
      const response = await apiService.decryptFile(filename);
      
      // Create blob and download
      const blob = new Blob([response.data], { type: 'text/plain' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename.replace('.encrypted', '');
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      if (onDecryptFile) {
        onDecryptFile(filename);
      }
      
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to decrypt file');
    } finally {
      setDecryptingFile(null);
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  if (loading) {
    return (
      <div className="card">
        <div className="loading">
          <div className="loading-spinner"></div>
          Loading encrypted files...
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card">
        <h2> Encrypted Files</h2>
        <div className="error">
          {error}
        </div>
        <button className="btn btn-secondary mt-2" onClick={fetchFiles}>
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="card">
      <div className="d-flex justify-between align-center mb-3">
        <h2> Encrypted Files ({files.length})</h2>
        <button className="btn btn-secondary btn-small" onClick={fetchFiles}>
           Refresh
        </button>
      </div>

      {files.length === 0 ? (
        <div className="info">
          No encrypted files found. Upload some files first.
        </div>
      ) : (
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Original File</th>
                <th>Size</th>
                <th>Upload Date</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {files.map((file, index) => (
                <tr key={index}>
                  <td>
                    <div className="file-name">{file.original_name}</div>
                    <div className="text-small text-muted">{file.filename}</div>
                  </td>
                  <td>{formatFileSize(file.size)}</td>
                  <td className="text-small">{formatDate(file.created)}</td>
                  <td>
                    <button
                      className="btn btn-warning btn-small"
                      onClick={() => handleDecrypt(file.filename)}
                      disabled={decryptingFile === file.filename}
                    >
                      {decryptingFile === file.filename ? (
                        <>
                          <div className="loading-spinner"></div>
                          Decrypting...
                        </>
                      ) : (
                        <>
                           Decrypt & Download
                        </>
                      )}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default FileList;
