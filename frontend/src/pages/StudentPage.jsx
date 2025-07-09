import React, { useState } from 'react';
import FileUploader from '../components/FileUploader';

const StudentPage = () => {
  const [uploadCount, setUploadCount] = useState(0);

  const handleUploadComplete = (uploadData) => {
    setUploadCount(prev => prev + uploadData.total_uploaded);
  };

  return (
    <div className="container">
      <div className="card text-center">
        <h1>🎓 Student Assignment Submission</h1>
        <p className="text-muted">
          Upload your assignment files securely. All files will be encrypted before storage.
        </p>
        {uploadCount > 0 && (
          <div className="success">
            ✅ Successfully submitted {uploadCount} assignment(s)
          </div>
        )}
      </div>

      <FileUploader onUploadComplete={handleUploadComplete} />

      <div className="card">
        <h3> Important Instructions</h3>
        <div style={{ background: '#f8f9ff', padding: '1.5rem', borderRadius: '8px', marginTop: '1rem' }}>
          <ul style={{ marginLeft: '1rem', lineHeight: '1.6' }}>
            <li>Only <strong>.txt</strong> files are accepted</li>
            <li>Files are automatically <strong>encrypted</strong> upon upload for security</li>
            <li>Make sure your assignment is complete before submitting</li>
            <li>You can upload multiple files at once</li>
            <li>File names should be descriptive (e.g., "assignment1_john_doe.txt")</li>
          </ul>
        </div>
      </div>

      <div className="card">
        <h3> Security & Privacy</h3>
        <div style={{ background: '#f0f8ff', padding: '1.5rem', borderRadius: '8px', marginTop: '1rem' }}>
          <p>
            <strong>Your submissions are secure:</strong>
          </p>
          <ul style={{ marginLeft: '1rem', lineHeight: '1.6' }}>
            <li>Files are encrypted using <strong>AES-256</strong> encryption</li>
            <li>Only authorized administrators can decrypt and review submissions</li>
            <li>Original files are deleted after encryption</li>
            <li>Plagiarism detection is performed on temporary decrypted copies</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default StudentPage;
