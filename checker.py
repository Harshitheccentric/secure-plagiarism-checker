#!/usr/bin/env python3
"""
Main Plagiarism Detection System
Integrates AES encryption/decryption with KMP-based similarity detection
"""

import os
import sys
import glob
from itertools import combinations
import crypto_utils
import kmp

class PlagiarismChecker:
    def __init__(self, submissions_dir="submissions", decrypted_dir="decrypted"):
        self.submissions_dir = submissions_dir
        self.decrypted_dir = decrypted_dir
        self.create_directories()
    
    def create_directories(self):
        """Create necessary directories if they don't exist"""
        os.makedirs(self.submissions_dir, exist_ok=True)
        os.makedirs(self.decrypted_dir, exist_ok=True)
    
    def setup_demo_files(self):
        """Create demo submission files for testing"""
        print("📁 Setting up demo files...")
        
        demo_texts = {
            "student1.txt": """
The quick brown fox jumps over the lazy dog. This is a common sentence used in typography.
Machine learning is a subset of artificial intelligence that enables computers to learn without being explicitly programmed.
Data structures and algorithms are fundamental concepts in computer science.
Python is a high-level programming language known for its simplicity and readability.
            """.strip(),
            
            "student2.txt": """
A quick brown fox jumps over the lazy dog. This sentence is commonly used in typography and design.
Machine learning represents a subset of artificial intelligence allowing computers to learn without explicit programming.
Fundamental concepts in computer science include data structures and algorithms.
Python programming language is known for high-level features, simplicity and code readability.
            """.strip(),
            
            "student3.txt": """
The weather today is quite pleasant with sunny skies and mild temperatures.
Blockchain technology has revolutionized the way we think about digital transactions and security.
Quantum computing promises to solve complex problems that are intractable for classical computers.
The Internet of Things connects everyday devices to create smart environments.
            """.strip(),
            
            "student4.txt": """
The quick brown fox jumps over the lazy dog. This is a common sentence used in typography.
Artificial intelligence and machine learning are transforming various industries.
Understanding data structures and algorithms is crucial for software development.
Programming languages like Python offer simplicity and powerful capabilities.
            """.strip(),
            
            "student5.txt": """
Sunny weather with mild temperatures makes for a pleasant day outside.
Digital transactions have been revolutionized by blockchain technology and its security features.
Complex computational problems may find solutions through quantum computing advances.
Smart environments emerge when Internet of Things connects various everyday devices.
            """.strip()
        }
        
        # Write demo files
        for filename, content in demo_texts.items():
            filepath = os.path.join(self.submissions_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✓ Created: {filepath}")
    
    def encrypt_submissions(self):
        """Encrypt all .txt files in submissions directory"""
        print("\n🔒 Encrypting submission files...")
        
        txt_files = glob.glob(os.path.join(self.submissions_dir, "*.txt"))
        if not txt_files:
            print("  ⚠️  No .txt files found in submissions directory")
            return []
        
        encrypted_files = []
        for txt_file in txt_files:
            encrypted_path = crypto_utils.encrypt_file(txt_file)
            if encrypted_path:
                encrypted_files.append(encrypted_path)
                # Remove original .txt file to simulate secure storage
                os.remove(txt_file)
        
        return encrypted_files
    
    def decrypt_submissions(self):
        """Decrypt all encrypted files for processing"""
        print("\n🔓 Decrypting files for analysis...")
        
        encrypted_files = glob.glob(os.path.join(self.submissions_dir, "*.encrypted"))
        if not encrypted_files:
            print("  ⚠️  No encrypted files found")
            return []
        
        decrypted_files = []
        for encrypted_file in encrypted_files:
            # Create output path in decrypted directory
            filename = os.path.basename(encrypted_file).replace('.txt.encrypted', '.txt')
            output_path = os.path.join(self.decrypted_dir, filename)
            
            decrypted_path = crypto_utils.decrypt_file(encrypted_file, output_path)
            if decrypted_path:
                decrypted_files.append(decrypted_path)
        
        return decrypted_files
    
    def load_file_content(self, filepath):
        """Load content from a text file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            print(f"  ✗ Error reading {filepath}: {e}")
            return None
    
    def run_plagiarism_check(self, method='word_based'):
        """Run plagiarism detection on all decrypted files"""
        print(f"\n🔍 Running plagiarism detection (method: {method})...")
        
        # Get all decrypted files
        decrypted_files = glob.glob(os.path.join(self.decrypted_dir, "*.txt"))
        
        if len(decrypted_files) < 2:
            print("  ⚠️  Need at least 2 files for comparison")
            return
        
        # Load file contents
        file_contents = {}
        for filepath in decrypted_files:
            filename = os.path.basename(filepath)
            content = self.load_file_content(filepath)
            if content:
                file_contents[filename] = content
        
        if len(file_contents) < 2:
            print("  ✗ Could not load enough files for comparison")
            return
        
        print(f"  📊 Comparing {len(file_contents)} files...")
        
        # Compare all pairs of files
        results = []
        file_names = list(file_contents.keys())
        
        for file1, file2 in combinations(file_names, 2):
            content1 = file_contents[file1]
            content2 = file_contents[file2]
            
            # Calculate similarity using KMP-based algorithm
            similarity_data = kmp.plagiarism_score(content1, content2, method)
            
            results.append({
                'file1': file1,
                'file2': file2,
                'similarity': similarity_data['similarity_percentage'],
                'common_segments': similarity_data['common_segments'],
                'method': similarity_data['method']
            })
        
        # Display results
        self.display_results(results)
        
        return results
    
    def display_results(self, results):
        """Display plagiarism detection results in a formatted table"""
        print("\n" + "="*80)
        print("🎯 PLAGIARISM DETECTION RESULTS")
        print("="*80)
        
        # Sort results by similarity (descending)
        results.sort(key=lambda x: x['similarity'], reverse=True)
        
        print(f"{'File 1':<20} {'File 2':<20} {'Similarity':<12} {'Segments':<10} {'Status'}")
        print("-" * 80)
        
        for result in results:
            file1 = result['file1'][:18] + ".." if len(result['file1']) > 20 else result['file1']
            file2 = result['file2'][:18] + ".." if len(result['file2']) > 20 else result['file2']
            similarity = f"{result['similarity']:.1f}%"
            segments = str(result['common_segments'])
            
            # Determine status based on similarity
            if result['similarity'] >= 80:
                status = "🚨 HIGH"
            elif result['similarity'] >= 50:
                status = "⚠️  MEDIUM"
            elif result['similarity'] >= 20:
                status = "ℹ️  LOW"
            else:
                status = "✅ MINIMAL"
            
            print(f"{file1:<20} {file2:<20} {similarity:<12} {segments:<10} {status}")
        
        print("-" * 80)
        print(f"Method used: {results[0]['method'] if results else 'N/A'}")
        
        # Summary statistics
        if results:
            avg_similarity = sum(r['similarity'] for r in results) / len(results)
            max_similarity = max(r['similarity'] for r in results)
            suspicious_pairs = len([r for r in results if r['similarity'] >= 50])
            
            print(f"\n📈 SUMMARY:")
            print(f"  • Average similarity: {avg_similarity:.1f}%")
            print(f"  • Highest similarity: {max_similarity:.1f}%")
            print(f"  • Suspicious pairs (≥50%): {suspicious_pairs}")
    
    def cleanup(self):
        """Clean up temporary decrypted files"""
        print("\n🧹 Cleaning up temporary files...")
        
        decrypted_files = glob.glob(os.path.join(self.decrypted_dir, "*.txt"))
        for file in decrypted_files:
            try:
                os.remove(file)
                print(f"  ✓ Removed: {os.path.basename(file)}")
            except Exception as e:
                print(f"  ✗ Failed to remove {file}: {e}")
    
    def run_full_pipeline(self, method='word_based', cleanup_after=True):
        """Run the complete plagiarism detection pipeline"""
        print("🚀 Starting Plagiarism Detection System")
        print("="*50)
        
        try:
            # Step 1: Setup demo files (if needed)
            '''
            if not glob.glob(os.path.join(self.submissions_dir, "*")):
                self.setup_demo_files()
            '''
            
            # Step 2: Encrypt submissions
            encrypted_files = self.encrypt_submissions()
            if not encrypted_files:
                print("❌ No files to encrypt. Exiting.")
                return
            
            # Step 3: Decrypt for analysis
            decrypted_files = self.decrypt_submissions()
            if not decrypted_files:
                print("❌ Decryption failed. Exiting.")
                return
            
            # Step 4: Run plagiarism detection
            results = self.run_plagiarism_check(method)
            
            # Step 5: Cleanup (optional)
            if cleanup_after:
                self.cleanup()
            
            print("\n✅ Plagiarism detection completed successfully!")
            return results
            
        except Exception as e:
            print(f"\n❌ Error in pipeline: {e}")
            return None

def main():
    """Main function to run the plagiarism detection system"""
    
    # Parse command line arguments
    method = 'word_based'  # Default method
    cleanup = True
    
    if len(sys.argv) > 1:
        if sys.argv[1] in ['word_based', 'char_based', 'line_based']:
            method = sys.argv[1]
        elif sys.argv[1] == '--help':
            print("Usage: python checker.py [method] [--no-cleanup]")
            print("Methods: word_based (default), char_based, line_based")
            print("Options: --no-cleanup (keep decrypted files)")
            return
    
    if '--no-cleanup' in sys.argv:
        cleanup = False
    
    # Initialize and run the plagiarism checker
    checker = PlagiarismChecker()
    results = checker.run_full_pipeline(method=method, cleanup_after=cleanup)
    
    if results:
        print(f"\n📊 Processed {len(results)} file pairs using {method} method")
    else:
        print("\n❌ Plagiarism detection failed")

if __name__ == "__main__":
    main()