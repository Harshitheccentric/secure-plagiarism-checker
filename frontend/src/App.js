import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import StudentPage from './pages/StudentPage';
import AdminPage from './pages/AdminPage';
import './styles/App.css';

const Navigation = () => {
  const location = useLocation();
  
  return (
    <nav className="navbar">
      <div className="navbar-content">
        <h1> Secure Plagiarism Checker</h1>
        <nav>
          <Link 
            to="/student" 
            className={location.pathname === '/student' ? 'active' : ''}
          >
             Student Portal
          </Link>
          <Link 
            to="/admin" 
            className={location.pathname === '/admin' ? 'active' : ''}
          >
             Admin Dashboard
          </Link>
        </nav>
      </div>
    </nav>
  );
};

const HomePage = () => {
  return (
    <div className="container">
      <div className="card text-center">
        <h1> Secure Plagiarism Detection System</h1>
        <p style={{ fontSize: '1.2rem', color: '#7f8c8d', marginBottom: '2rem' }}>
          A secure platform for assignment submission and plagiarism detection using AES encryption and KMP string matching
        </p>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem', marginTop: '2rem' }}>
          <Link to="/student" className="btn btn-primary" style={{ padding: '2rem', textDecoration: 'none' }}>
            <div>
              <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🎓</div>
              <h3>Student Portal</h3>
              <p style={{ color: 'rgba(255,255,255,0.9)', margin: '0.5rem 0 0 0' }}>
                Upload and submit your assignments securely
              </p>
            </div>
          </Link>
          
          <Link to="/admin" className="btn btn-primary" style={{ padding: '2rem', textDecoration: 'none' }}>
            <div>
              <div style={{ fontSize: '3rem', marginBottom: '1rem' }}></div>
              <h3>Admin Dashboard</h3>
              <p style={{ color: 'rgba(255,255,255,0.9)', margin: '0.5rem 0 0 0' }}>
                Manage submissions and detect plagiarism
              </p>
            </div>
          </Link>
        </div>
      </div>
      
      <div className="card">
        <h2> System Features</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1.5rem', marginTop: '1.5rem' }}>
          <div>
            <h4> AES-256 Encryption</h4>
            <p className="text-muted">
              All uploaded files are encrypted using industry-standard AES-256-CBC encryption with random initialization vectors.
            </p>
          </div>
          
          <div>
            <h4> KMP Algorithm</h4>
            <p className="text-muted">
              Advanced plagiarism detection using the Knuth-Morris-Pratt string matching algorithm for accurate similarity analysis.
            </p>
          </div>
          
          <div>
            <h4> Multiple Detection Methods</h4>
            <p className="text-muted">
              Choose from word-based, character-based, or line-based similarity detection methods for comprehensive analysis.
            </p>
          </div>
          
          <div>
            <h4> Secure File Handling</h4>
            <p className="text-muted">
              Original files are deleted after encryption, and temporary decrypted files are automatically cleaned up.
            </p>
          </div>
          
          <div>
            <h4> Detailed Reports</h4>
            <p className="text-muted">
              Generate comprehensive plagiarism reports with similarity percentages, statistics, and downloadable JSON exports.
            </p>
          </div>
          
          <div>
            <h4> Web-based Interface</h4>
            <p className="text-muted">
              User-friendly React frontend with separate portals for students and administrators with real-time updates.
            </p>
          </div>
        </div>
      </div>
      
      <div className="card">
        <h2> Workflow Overview</h2>
        <div style={{ background: '#f8f9ff', padding: '1.5rem', borderRadius: '8px', marginTop: '1rem' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <div style={{ background: '#667eea', color: 'white', borderRadius: '50%', width: '30px', height: '30px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold' }}>1</div>
              <div>Students upload .txt assignment files through the secure portal</div>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <div style={{ background: '#667eea', color: 'white', borderRadius: '50%', width: '30px', height: '30px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold' }}>2</div>
              <div>Files are automatically encrypted using AES-256 and stored securely</div>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <div style={{ background: '#667eea', color: 'white', borderRadius: '50%', width: '30px', height: '30px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold' }}>3</div>
              <div>Administrators can decrypt individual files or generate plagiarism reports</div>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <div style={{ background: '#667eea', color: 'white', borderRadius: '50%', width: '30px', height: '30px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold' }}>4</div>
              <div>KMP algorithm analyzes all file pairs for similarity detection</div>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <div style={{ background: '#667eea', color: 'white', borderRadius: '50%', width: '30px', height: '30px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold' }}>5</div>
              <div>Comprehensive reports are generated with similarity scores and statistics</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

function App() {
  return (
    <Router>
      <div className="App">
        <Navigation />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/student" element={<StudentPage />} />
          <Route path="/admin" element={<AdminPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
