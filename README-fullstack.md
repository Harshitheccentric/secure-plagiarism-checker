# Secure Plagiarism Detection System - Full Stack Web Application

A complete web-based plagiarism detection system with AES encryption and KMP string matching algorithm.

## 🏗️ Project Structure

```
secure-plagiarism-checker/
├── backend/                 # Flask API Server
│   ├── app.py              # Main Flask application
│   ├── crypto_utils.py     # AES encryption/decryption
│   ├── plagiarism.py       # KMP-based plagiarism detection
│   ├── requirements.txt    # Python dependencies
│   ├── submissions/        # Encrypted student files
│   ├── decrypted/         # Temporary decrypted files
│   └── reports/           # Generated plagiarism reports
├── frontend/               # React Web Application
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── styles/        # CSS styles
│   │   ├── App.js         # Main React app
│   │   ├── index.js       # React entry point
│   │   └── apiService.js  # API communication
│   ├── public/
│   └── package.json       # Node.js dependencies
└── README-fullstack.md    # This documentation
```

## 🚀 Quick Start

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Flask server:**
   ```bash
   python app.py
   ```
   
   The API will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Start the React development server:**
   ```bash
   npm start
   ```
   
   The web application will be available at `http://localhost:3000`

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | System health check |
| `POST` | `/api/upload` | Upload and encrypt files |
| `GET` | `/api/files` | List encrypted files |
| `POST` | `/api/decrypt` | Decrypt specific file |
| `POST` | `/api/decrypt-all` | Decrypt all files |
| `GET` | `/api/report` | Generate plagiarism report |
| `GET` | `/api/reports` | List saved reports |
| `POST` | `/api/cleanup` | Clean temporary files |

## 🎯 Features

### Student Portal (`/student`)
- **Secure File Upload:** Drag & drop or click to upload .txt files
- **Automatic Encryption:** Files are encrypted using AES-256-CBC
- **Progress Tracking:** Real-time upload status and feedback
- **File Validation:** Only .txt files accepted

### Admin Dashboard (`/admin`)
- **File Management:** View all encrypted submissions
- **Selective Decryption:** Decrypt and download individual files
- **Plagiarism Analysis:** Generate comprehensive similarity reports
- **Multiple Detection Methods:**
  - Word-based analysis (default)
  - Character-based analysis
  - Line-based analysis
- **System Maintenance:** Health checks and cleanup utilities

### Security Features
- **AES-256-CBC Encryption** with random IV per file
- **Automatic File Cleanup** after processing
- **Secure File Handling** with proper error handling
- **No Persistent Decrypted Storage**

## 🔍 Plagiarism Detection

### Detection Methods

1. **Word-based Analysis (Recommended)**
   - Analyzes word sequences and phrases
   - Detects paraphrasing and structural similarities
   - Best for academic text analysis

2. **Character-based Analysis**
   - Finds longest common substrings
   - Sensitive to exact character matches
   - Good for detecting copy-paste plagiarism

3. **Line-based Analysis**
   - Compares exact line matches
   - Fastest method for identical content detection
   - Less sensitive to minor modifications

### Similarity Thresholds

| Threshold | Status | Description |
|-----------|--------|-------------|
| ≥80% | 🚨 HIGH | Likely plagiarism - requires investigation |
| 50-79% | ⚠️ MEDIUM | Suspicious similarities - review recommended |
| 20-49% | ℹ️ LOW | Some overlap - may be acceptable |
| <20% | ✅ MINIMAL | Minimal similarity - likely original work |

## 🛠️ Development

### Backend Development

- **Framework:** Flask with CORS support
- **Encryption:** PyCryptodome for AES operations
- **File Handling:** Werkzeug for secure uploads
- **API Design:** RESTful endpoints with JSON responses

### Frontend Development

- **Framework:** React 18 with React Router
- **HTTP Client:** Axios for API communication
- **Styling:** CSS modules with responsive design
- **Components:** Modular, reusable components

### Running in Development Mode

Both servers support hot-reload for development:

- **Backend:** Flask runs with `debug=True`
- **Frontend:** React development server with proxy to backend

## 📊 Example Usage Workflow

1. **Student uploads files** via the web interface
2. **Files are encrypted** and stored securely on the server
3. **Admin generates report** using the desired detection method
4. **System analyzes** all file pairs using KMP algorithm
5. **Comprehensive report** is generated with similarity scores
6. **Admin reviews results** and takes appropriate action

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory for production:

```env
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
AES_KEY=your-32-byte-aes-key-here
```

### Frontend Configuration

Update `src/apiService.js` for production API URL:

```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://your-api-domain.com/api';
```

## 📈 Performance Considerations

- **File Size Limits:** Recommended maximum 10MB per file
- **Concurrent Users:** Flask development server supports limited concurrency
- **Memory Usage:** Large files may require increased server memory
- **Processing Time:** Character-based analysis may take longer for large files

## 🔒 Security Best Practices

1. **Use HTTPS** in production environments
2. **Implement authentication** for admin access
3. **Regular key rotation** for encryption keys
4. **Monitor file storage** and implement size limits
5. **Audit logs** for file access and operations

## 🚀 Deployment

### Backend Deployment
- Use **Gunicorn** or **uWSGI** for production WSGI server
- Configure **nginx** as reverse proxy
- Use **PostgreSQL** or **MySQL** for persistent data storage

### Frontend Deployment
- Build with `npm run build`
- Serve static files with **nginx** or **Apache**
- Configure **CDN** for better performance

## 📝 License

This project is for educational purposes and demonstrates secure file handling and plagiarism detection techniques.
