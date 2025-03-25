import requests
import os
import hmac
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

SERVER_URL = 'http://localhost:5000'
key = b'my_fixed_shared_secret_key_12345'  # Shared secret key for HMAC
aes_key = os.urandom(32)   # Fixed 32-byte AES key (valid size for AES-256)

def encrypt_file(file_data):
    """Encrypt the file data using AES encryption."""
    iv = os.urandom(16)  # Initialization vector
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(file_data) + encryptor.finalize()
    return iv + encrypted_data  # Prepend IV to the encrypted data for later decryption

def decrypt_file(encrypted_data):
    """Decrypt the file data using AES."""
    iv = encrypted_data[:16]  # Extract the IV
    encrypted_file_data = encrypted_data[16:]  # Extract the encrypted part

    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(encrypted_file_data) + decryptor.finalize()

def upload_file(file_path):
    """Upload file to the server with HMAC for integrity verification."""
    with open(file_path, 'rb') as file:
        file_data = file.read()

    # Encrypt file before upload
    encrypted_file_data = encrypt_file(file_data)

    # Calculate HMAC for integrity
    hmac_signature = hmac.new(key, encrypted_file_data, hashlib.sha256).hexdigest()
    print("Sending HMAC for upload:", hmac_signature)

    # Send file to server with HMAC for integrity verification
    files = {'file': (os.path.basename(file_path), encrypted_file_data)}
    headers = {'HMAC-Signature': hmac_signature}
    response = requests.post(f"{SERVER_URL}/upload", files=files, headers=headers)
    
    print("Raw response from server:", response.text)
    try:
        print(response.json())
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON from the server response")

def download_file(filename):
    """Download file from the server and verify its integrity."""
    response = requests.get(f"{SERVER_URL}/download/{filename}")
    if response.status_code == 200:
        hmac_signature = response.headers.get('HMAC-Signature')
        encrypted_file_data = response.content

        # Verify HMAC before decryption
        computed_hmac = hmac.new(key, encrypted_file_data, hashlib.sha256).hexdigest()
        print("Server HMAC:", hmac_signature)
        print("Computed HMAC:", computed_hmac)

        if computed_hmac == hmac_signature:
            # Decrypt the file after verifying integrity
            file_data = decrypt_file(encrypted_file_data)

            # Save downloaded file
            with open(f"downloaded_{filename}", 'wb') as f:
                f.write(file_data)
            print(f"File {filename} downloaded and integrity verified.")
        else:
            print("Integrity check failed for the downloaded file.")
    else:
        print("File not found or download failed.")

if __name__ == "__main__":
    upload_file('testfile.txt')  # Test file upload
    download_file('testfile.txt')  # Test file download
