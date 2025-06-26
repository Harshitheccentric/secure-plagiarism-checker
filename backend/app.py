"""
Flask backend for secure plagiarism detection system
"""

import os
import glob
import json
from datetime import datetime
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import crypto_utils
import plagiarism

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend interaction

# Configuration
UPLOAD_FOLDER = 'submissions'
DECRYPTED_FOLDER = 'decrypted'
REPORTS_FOLDER = 'reports'
ALLOWED_EXTENSIONS = {'txt'}

# Ensure directories exist
for folder in [UPLOAD_FOLDER, DECRYPTED_FOLDER, REPORTS_FOLDER]:
    os.makedirs(folder, exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_status_from_similarity(similarity):
    """Get status label based on similarity percentage"""
    if similarity >= 80:
        return "HIGH"
    elif similarity >= 50:
        return "MEDIUM"
    elif similarity >= 20:
        return "LOW"
    else:
        return "MINIMAL"

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Plagiarism Detection API is running',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/upload', methods=['POST'])
def upload_files():
    """
    Upload and encrypt text files
    
    Expected: multipart/form-data with 'files' field
    Returns: JSON with upload status and file info
    """
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        if not files or all(f.filename == '' for f in files):
            return jsonify({'error': 'No files selected'}), 400
        
        uploaded_files = []
        errors = []
        
        for file in files:
            if file and file.filename and allowed_file(file.filename):
                # Secure the filename
                filename = secure_filename(file.filename)
                
                # Save temporary file
                temp_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(temp_path)
                
                # Encrypt the file
                encrypted_path = os.path.join(UPLOAD_FOLDER, filename + '.encrypted')
                result = crypto_utils.encrypt_file(temp_path, encrypted_path)
                
                if result:
                    # Remove the temporary unencrypted file
                    os.remove(temp_path)
                    
                    uploaded_files.append({
                        'original_name': file.filename,
                        'encrypted_name': filename + '.encrypted',
                        'size': os.path.getsize(encrypted_path),
                        'status': 'encrypted'
                    })
                else:
                    errors.append(f"Failed to encrypt {filename}")
            else:
                errors.append(f"Invalid file type: {file.filename}")
        
        response = {
            'message': f'Successfully uploaded {len(uploaded_files)} files',
            'uploaded_files': uploaded_files,
            'total_uploaded': len(uploaded_files)
        }
        
        if errors:
            response['errors'] = errors
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/api/files', methods=['GET'])
def list_files():
    """
    List all encrypted files in submissions directory
    
    Returns: JSON list of file information
    """
    try:
        encrypted_files = glob.glob(os.path.join(UPLOAD_FOLDER, "*.encrypted"))
        
        files_info = []
        for filepath in encrypted_files:
            filename = os.path.basename(filepath)
            original_name = filename.replace('.encrypted', '') if filename.endswith('.encrypted') else filename
            
            files_info.append({
                'filename': filename,
                'original_name': original_name,
                'size': os.path.getsize(filepath),
                'created': datetime.fromtimestamp(os.path.getctime(filepath)).isoformat(),
                'path': filepath
            })
        
        # Sort by creation date (newest first)
        files_info.sort(key=lambda x: x['created'], reverse=True)
        
        return jsonify({
            'files': files_info,
            'total_files': len(files_info)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to list files: {str(e)}'}), 500

@app.route('/api/decrypt', methods=['POST'])
def decrypt_file():
    """
    Decrypt a specific file and return it for download
    
    Expected JSON: {'filename': 'example.txt.encrypted'}
    Returns: File download or error
    """
    try:
        data = request.get_json()
        if not data or 'filename' not in data:
            return jsonify({'error': 'Filename required'}), 400
        
        filename = data['filename']
        encrypted_path = os.path.join(UPLOAD_FOLDER, filename)
        
        if not os.path.exists(encrypted_path):
            return jsonify({'error': 'File not found'}), 404
        
        # Create decrypted filename
        if filename.endswith('.encrypted'):
            decrypted_filename = filename[:-10]  # Remove '.encrypted'
        else:
            decrypted_filename = filename + '.decrypted'
        
        decrypted_path = os.path.join(DECRYPTED_FOLDER, decrypted_filename)
        
        # Decrypt the file
        result = crypto_utils.decrypt_file(encrypted_path, decrypted_path)
        
        if result:
            return send_file(
                decrypted_path,
                as_attachment=True,
                download_name=decrypted_filename,
                mimetype='text/plain'
            )
        else:
            return jsonify({'error': 'Decryption failed'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Decryption failed: {str(e)}'}), 500

@app.route('/api/decrypt-all', methods=['POST'])
def decrypt_all_files():
    """
    Decrypt all encrypted files for plagiarism analysis
    
    Returns: JSON with decryption status
    """
    try:
        encrypted_files = glob.glob(os.path.join(UPLOAD_FOLDER, "*.encrypted"))
        
        if not encrypted_files:
            return jsonify({'error': 'No encrypted files found'}), 404
        
        decrypted_files = []
        errors = []
        
        for encrypted_path in encrypted_files:
            filename = os.path.basename(encrypted_path)
            
            # Create decrypted filename
            if filename.endswith('.encrypted'):
                decrypted_filename = filename[:-10]  # Remove '.encrypted'
            else:
                decrypted_filename = filename + '.decrypted'
            
            decrypted_path = os.path.join(DECRYPTED_FOLDER, decrypted_filename)
            
            # Decrypt the file
            result = crypto_utils.decrypt_file(encrypted_path, decrypted_path)
            
            if result:
                decrypted_files.append({
                    'original': filename,
                    'decrypted': decrypted_filename,
                    'path': result
                })
            else:
                errors.append(f"Failed to decrypt {filename}")
        
        response = {
            'message': f'Successfully decrypted {len(decrypted_files)} files',
            'decrypted_files': decrypted_files,
            'total_decrypted': len(decrypted_files)
        }
        
        if errors:
            response['errors'] = errors
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': f'Batch decryption failed: {str(e)}'}), 500

@app.route('/api/report', methods=['GET', 'POST'])
def generate_report():
    """
    Generate plagiarism detection report
    
    Optional JSON body: {'method': 'word_based'|'char_based'|'line_based'}
    Returns: JSON plagiarism report
    """
    try:
        # Get method from request (default to word_based)
        method = 'word_based'
        if request.is_json and request.get_json():
            data = request.get_json()
            method = data.get('method', 'word_based')
        elif request.args.get('method'):
            method = request.args.get('method')
        
        # First, decrypt all files
        encrypted_files = glob.glob(os.path.join(UPLOAD_FOLDER, "*.encrypted"))
        
        if len(encrypted_files) < 2:
            return jsonify({
                'error': 'Need at least 2 encrypted files for plagiarism detection',
                'files_found': len(encrypted_files)
            }), 400
        
        # Decrypt files for analysis
        decrypted_count = 0
        for encrypted_path in encrypted_files:
            filename = os.path.basename(encrypted_path)
            
            if filename.endswith('.encrypted'):
                decrypted_filename = filename[:-10]  # Remove '.encrypted'
            else:
                decrypted_filename = filename + '.decrypted'
            
            decrypted_path = os.path.join(DECRYPTED_FOLDER, decrypted_filename)
            
            # Only decrypt if not already decrypted
            if not os.path.exists(decrypted_path):
                result = crypto_utils.decrypt_file(encrypted_path, decrypted_path)
                if result:
                    decrypted_count += 1
        
        # Run plagiarism detection
        results = plagiarism.run_plagiarism_check(DECRYPTED_FOLDER, method)
        
        if not results:
            return jsonify({
                'error': 'Failed to generate plagiarism report',
                'decrypted_files': decrypted_count
            }), 500
        
        # Add status labels and prepare summary
        for result in results:
            result['status'] = get_status_from_similarity(result['similarity'])
        
        # Calculate summary statistics
        total_comparisons = len(results)
        avg_similarity = sum(r['similarity'] for r in results) / total_comparisons if total_comparisons > 0 else 0
        max_similarity = max(r['similarity'] for r in results) if results else 0
        
        suspicious_pairs = len([r for r in results if r['similarity'] >= 50])
        high_risk_pairs = len([r for r in results if r['similarity'] >= 80])
        
        # Create report
        report = {
            'timestamp': datetime.now().isoformat(),
            'method': method,
            'summary': {
                'total_files': len(encrypted_files),
                'total_comparisons': total_comparisons,
                'average_similarity': round(avg_similarity, 2),
                'highest_similarity': round(max_similarity, 2),
                'suspicious_pairs': suspicious_pairs,
                'high_risk_pairs': high_risk_pairs
            },
            'comparisons': results
        }
        
        # Save report to file
        report_filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{method}.json"
        report_path = os.path.join(REPORTS_FOLDER, report_filename)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        report['report_saved'] = report_filename
        
        return jsonify(report), 200
        
    except Exception as e:
        return jsonify({'error': f'Report generation failed: {str(e)}'}), 500

@app.route('/api/cleanup', methods=['POST'])
def cleanup_decrypted():
    """
    Clean up temporary decrypted files
    
    Returns: JSON with cleanup status
    """
    try:
        decrypted_files = glob.glob(os.path.join(DECRYPTED_FOLDER, "*.txt"))
        
        removed_count = 0
        errors = []
        
        for filepath in decrypted_files:
            try:
                os.remove(filepath)
                removed_count += 1
            except Exception as e:
                errors.append(f"Failed to remove {os.path.basename(filepath)}: {str(e)}")
        
        response = {
            'message': f'Cleaned up {removed_count} temporary files',
            'removed_count': removed_count
        }
        
        if errors:
            response['errors'] = errors
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': f'Cleanup failed: {str(e)}'}), 500

@app.route('/api/reports', methods=['GET'])
def list_reports():
    """
    List all saved reports
    
    Returns: JSON list of available reports
    """
    try:
        report_files = glob.glob(os.path.join(REPORTS_FOLDER, "*.json"))
        
        reports_info = []
        for filepath in report_files:
            filename = os.path.basename(filepath)
            
            reports_info.append({
                'filename': filename,
                'size': os.path.getsize(filepath),
                'created': datetime.fromtimestamp(os.path.getctime(filepath)).isoformat(),
                'path': filepath
            })
        
        # Sort by creation date (newest first)
        reports_info.sort(key=lambda x: x['created'], reverse=True)
        
        return jsonify({
            'reports': reports_info,
            'total_reports': len(reports_info)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to list reports: {str(e)}'}), 500

@app.route('/api/reports/<filename>', methods=['GET'])
def download_report(filename):
    """
    Download a specific report file
    
    Args:
        filename: Name of the report file
    
    Returns: File download
    """
    try:
        return send_from_directory(
            REPORTS_FOLDER,
            filename,
            as_attachment=True,
            mimetype='application/json'
        )
    except Exception as e:
        return jsonify({'error': f'Failed to download report: {str(e)}'}), 404

if __name__ == '__main__':
    print("🚀 Starting Plagiarism Detection API Server")
    print("📁 Directories:")
    print(f"   - Submissions: {os.path.abspath(UPLOAD_FOLDER)}")
    print(f"   - Decrypted: {os.path.abspath(DECRYPTED_FOLDER)}")
    print(f"   - Reports: {os.path.abspath(REPORTS_FOLDER)}")
    print("\n🔗 API Endpoints:")
    print("   - POST /api/upload       - Upload and encrypt files")
    print("   - GET  /api/files        - List encrypted files")
    print("   - POST /api/decrypt      - Decrypt specific file")
    print("   - POST /api/decrypt-all  - Decrypt all files")
    print("   - GET  /api/report       - Generate plagiarism report")
    print("   - POST /api/cleanup      - Clean temporary files")
    print("   - GET  /api/reports      - List saved reports")
    print("\n🌐 Server starting on http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
