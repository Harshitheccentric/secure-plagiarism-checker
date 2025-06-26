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
        str: Path to the encrypted file, or None if failed
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

def encrypt_content(content):
    """
    Encrypt string content directly
    
    Args:
        content (str): Text content to encrypt
    
    Returns:
        bytes: Encrypted content (IV + ciphertext), or None if failed
    """
    try:
        # Convert to bytes
        plaintext_bytes = content.encode('utf-8')
        
        # Generate random IV (16 bytes for AES)
        iv = get_random_bytes(16)
        
        # Create cipher object
        cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
        
        # Pad and encrypt
        padded_data = pad(plaintext_bytes, AES.block_size)
        ciphertext = cipher.encrypt(padded_data)
        
        return iv + ciphertext
        
    except Exception as e:
        print(f"✗ Content encryption failed: {e}")
        return None

def decrypt_content(encrypted_data):
    """
    Decrypt encrypted bytes directly
    
    Args:
        encrypted_data (bytes): Encrypted content (IV + ciphertext)
    
    Returns:
        str: Decrypted text content, or None if failed
    """
    try:
        # Extract IV (first 16 bytes) and ciphertext
        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]
        
        # Create cipher object
        cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
        
        # Decrypt and unpad
        padded_plaintext = cipher.decrypt(ciphertext)
        plaintext_bytes = unpad(padded_plaintext, AES.block_size)
        
        # Convert back to string
        return plaintext_bytes.decode('utf-8')
        
    except Exception as e:
        print(f"✗ Content decryption failed: {e}")
        return None
