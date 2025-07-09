import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds timeout
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(` API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for logging
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('❌ API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const apiService = {
  // Health check
  healthCheck: () => api.get('/health'),

  // File upload
  uploadFiles: (files) => {
    const formData = new FormData();
    Array.from(files).forEach((file) => {
      formData.append('files', file);
    });
    
    return api.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  // List encrypted files
  getFiles: () => api.get('/files'),

  // Decrypt specific file
  decryptFile: (filename) => 
    api.post('/decrypt', { filename }, {
      responseType: 'blob',
    }),

  // Decrypt all files
  decryptAllFiles: () => api.post('/decrypt-all'),

  // Generate plagiarism report
  generateReport: (method = 'word_based') => 
    api.get('/report', { params: { method } }),

  // Get saved reports
  getReports: () => api.get('/reports'),

  // Download report
  downloadReport: (filename) => 
    api.get(`/reports/${filename}`, {
      responseType: 'blob',
    }),

  // Clean up temporary files
  cleanup: () => api.post('/cleanup'),

  // Save matched sequences
  saveMatchedSequences: async (matchData) => {
    try {
      const response = await fetch(`${API_BASE_URL}/save-matches`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(matchData),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error saving matched sequences:', error);
      throw error;
    }
  },

  // Get matched sequences
  getMatchedSequences: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/matches`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error fetching matched sequences:', error);
      throw error;
    }
  },

  // Download match file
  downloadMatchFile: async (filename) => {
    try {
      const response = await fetch(`${API_BASE_URL}/matches/${filename}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Error downloading match file:', error);
      throw error;
    }
  },
};

export default apiService;
