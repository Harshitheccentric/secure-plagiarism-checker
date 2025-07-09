import React, { useState, useRef } from 'react';
import apiService from '../apiService';

const FileUploader = ({ onUploadComplete }) => {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(null);
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileSelect = (files) => {
    const txtFiles = Array.from(files).filter(file => 
      file.type === 'text/plain' || file.name.endsWith('.txt')
    );
    
    if (txtFiles.length !== files.length) {
      setUploadStatus({
        type: 'warning',
        message: 'Only .txt files are allowed. Some files were filtered out.'
      });
    }
    
    setSelectedFiles(txtFiles);
  };

  const handleFileInputChange = (e) => {
    handleFileSelect(e.target.files);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    handleFileSelect(e.dataTransfer.files);
  };

  const handleUpload = async () => {
    if (selectedFiles.length === 0) {
      setUploadStatus({
        type: 'warning',
        message: 'Please select at least one file to upload.'
      });
      return;
    }

    setUploading(true);
    setUploadStatus(null);

    try {
      const response = await apiService.uploadFiles(selectedFiles);
      
      setUploadStatus({
        type: 'success',
        message: `Successfully uploaded ${response.data.total_uploaded} files and encrypted them.`
      });
      
      setSelectedFiles([]);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
      
      if (onUploadComplete) {
        onUploadComplete(response.data);
      }
      
    } catch (error) {
      setUploadStatus({
        type: 'error',
        message: error.response?.data?.error || 'Upload failed. Please try again.'
      });
    } finally {
      setUploading(false);
    }
  };

  const removeFile = (index) => {
    const newFiles = selectedFiles.filter((_, i) => i !== index);
    setSelectedFiles(newFiles);
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="card">
      <h2> Upload Assignment Files</h2>
      
      <div 
        className={`file-upload-area ${dragOver ? 'dragover' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <div className="file-upload-icon">📄</div>
        <div className="file-upload-text">
          Drag & drop your .txt files here
        </div>
        <div className="file-upload-hint">
          or click to select files
        </div>
        
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept=".txt"
          onChange={handleFileInputChange}
          style={{ display: 'none' }}
        />
      </div>

      {selectedFiles.length > 0 && (
        <div className="file-list">
          <h3>Selected Files ({selectedFiles.length})</h3>
          {selectedFiles.map((file, index) => (
            <div key={index} className="file-item">
              <div>
                <div className="file-name">{file.name}</div>
                <div className="file-size">{formatFileSize(file.size)}</div>
              </div>
              <button 
                className="btn btn-danger btn-small"
                onClick={(e) => {
                  e.stopPropagation();
                  removeFile(index);
                }}
              >
                Remove
              </button>
            </div>
          ))}
          
          <div className="mt-3">
            <button 
              className="btn btn-primary"
              onClick={handleUpload}
              disabled={uploading}
            >
              {uploading ? (
                <>
                  <div className="loading-spinner"></div>
                  Encrypting & Uploading...
                </>
              ) : (
                <>
                   Encrypt & Upload Files
                </>
              )}
            </button>
          </div>
        </div>
      )}

      {uploadStatus && (
        <div className={uploadStatus.type}>
          {uploadStatus.message}
        </div>
      )}
    </div>
  );
};

export default FileUploader;
