"""
AES Encryption/Decryption utilities for secure plagiarism detection system
Uses AES-CBC mode with PKCS7 padding
"""

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import os

# Fixed key for demo purposes (32 bytes for AES-256)
AES_KEY = b'this_is_a_32_byte_key_for_demo!!'

def encrypt_file(input_path, output_path=None):
    """
    Encrypt a text file using AES-CBC encryption
    
    Args:
        input_path (str): Path to the input text file
        output_path (str): Path for encrypted output (optional)
    
    Returns:
        str: Path to the encrypted file
    """
    if output_path is None:
        output_path = input_path + '.encrypted'
    
    try:
        # Read the original file
        with open(input_path, 'r', encoding='utf-8') as f:
            plaintext = f.read()
        
        # Convert to bytes
        plaintext_bytes = plaintext.encode('utf-8')
        
        # Generate random IV (16 bytes for AES)
        iv = get_random_bytes(16)
        
        # Create cipher object
        cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
        
        # Pad and encrypt
        padded_data = pad(plaintext_bytes, AES.block_size)
        ciphertext = cipher.encrypt(padded_data)
        
        # Write IV + ciphertext to file
        with open(output_path, 'wb') as f:
            f.write(iv + ciphertext)
        
        print(f"✓ Encrypted: {input_path} -> {output_path}")
        return output_path
        
    except Exception as e:
        print(f"✗ Encryption failed for {input_path}: {e}")
        return None

def decrypt_file(input_path, output_path=None):
    """
    Decrypt an AES-encrypted file
    
    Args:
        input_path (str): Path to the encrypted file
        output_path (str): Path for decrypted output (optional)
    
    Returns:
        str: Path to the decrypted file, or None if failed
    """
    if output_path is None:
        # Remove .encrypted extension or add .decrypted
        if input_path.endswith('.encrypted'):
            output_path = input_path[:-10]  # Remove '.encrypted'
        else:
            output_path = input_path + '.decrypted'
    
    try:
        # Read encrypted file
        with open(input_path, 'rb') as f:
            encrypted_data = f.read()
        
        # Extract IV (first 16 bytes) and ciphertext
        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]
        
        # Create cipher object
        cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
        
        # Decrypt and unpad
        padded_plaintext = cipher.decrypt(ciphertext)
        plaintext_bytes = unpad(padded_plaintext, AES.block_size)
        
        # Convert back to string
        plaintext = plaintext_bytes.decode('utf-8')
        
        # Write decrypted content
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(plaintext)
        
        print(f"✓ Decrypted: {input_path} -> {output_path}")
        return output_path
        
    except Exception as e:
        print(f"✗ Decryption failed for {input_path}: {e}")
        return None

def encrypt_directory(directory_path, output_directory=None):
    """
    Encrypt all .txt files in a directory
    
    Args:
        directory_path (str): Path to directory containing .txt files
        output_directory (str): Output directory for encrypted files
    
    Returns:
        list: List of encrypted file paths
    """
    if output_directory is None:
        output_directory = os.path.join(directory_path, 'encrypted')
    
    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)
    
    encrypted_files = []
    
    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            input_path = os.path.join(directory_path, filename)
            output_path = os.path.join(output_directory, filename + '.encrypted')
            
            result = encrypt_file(input_path, output_path)
            if result:
                encrypted_files.append(result)
    
    return encrypted_files

def decrypt_directory(directory_path, output_directory=None):
    """
    Decrypt all .encrypted files in a directory
    
    Args:
        directory_path (str): Path to directory containing encrypted files
        output_directory (str): Output directory for decrypted files
    
    Returns:
        list: List of decrypted file paths
    """
    if output_directory is None:
        output_directory = os.path.join(os.path.dirname(directory_path), 'decrypted')
    
    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)
    
    decrypted_files = []
    
    for filename in os.listdir(directory_path):
        if filename.endswith('.encrypted'):
            input_path = os.path.join(directory_path, filename)
            # Remove .encrypted extension for output
            output_filename = filename[:-10] if filename.endswith('.encrypted') else filename + '.decrypted'
            output_path = os.path.join(output_directory, output_filename)
            
            result = decrypt_file(input_path, output_path)
            if result:
                decrypted_files.append(result)
    
    return decrypted_files

if __name__ == "__main__":
    # Test the encryption/decryption
    test_content = "This is a test file for encryption and decryption."
    
    # Create a test file
    with open("test.txt", "w") as f:
        f.write(test_content)
    
    # Test encryption
    encrypted_path = encrypt_file("test.txt")
    
    # Test decryption
    if encrypted_path:
        decrypted_path = decrypt_file(encrypted_path, "test_decrypted.txt")
        
        # Verify content
        if decrypted_path:
            with open(decrypted_path, "r") as f:
                decrypted_content = f.read()
            
            if decrypted_content == test_content:
                print("✓ Encryption/Decryption test passed!")
            else:
                print("✗ Content mismatch after decryption")
    
    # Clean up test files
    for file in ["test.txt", "test.txt.encrypted", "test_decrypted.txt"]:
        if os.path.exists(file):
            os.remove(file)