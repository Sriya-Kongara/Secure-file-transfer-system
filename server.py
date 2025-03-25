import os
import hmac
import hashlib
import io
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from flask import Flask, request, send_file, jsonify

# Server setup
app = Flask(__name__)
key = b'my_fixed_shared_secret_key_12345'  # Secret key for HMAC
aes_key = os.urandom(32)  # AES key for encryption

# Generate RSA key pair
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
public_key = private_key.public_key()

# Serialize and store the server's public key
public_key_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Ensure the 'server_files' directory exists
if not os.path.exists('server_files'):
    os.makedirs('server_files')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    hmac_signature = request.headers.get('HMAC-Signature')
    print("Received HMAC from client:", hmac_signature)

    # Read the file data
    file_data = file.read()

    # Validate HMAC for integrity
    computed_hmac = hmac.new(key, file_data, hashlib.sha256).hexdigest()
    print("Computed HMAC on server:", computed_hmac)

    if hmac_signature != computed_hmac:
        return jsonify({'status': 'failed', 'reason': 'Integrity check failed'}), 400

    # AES Encryption
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = iv + encryptor.update(file_data) + encryptor.finalize()

    # Save encrypted file
    file_path = os.path.join('server_files', file.filename)
    with open(file_path, 'wb') as f:
        f.write(encrypted_data)
    print(f"File saved at: {file_path}")  # Log file path

    return jsonify({'status': 'success', 'message': 'File uploaded and encrypted successfully'}), 200

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join('server_files', filename)
    print(f"Attempting to download: {file_path}")  # Log the file path
    
    if not os.path.exists(file_path):
        return jsonify({'status': 'failed', 'reason': 'File not found'}), 404

    with open(file_path, 'rb') as f:
        encrypted_data = f.read()

    # Decrypt data
    iv = encrypted_data[:16]
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data[16:]) + decryptor.finalize()

    # Calculate HMAC for integrity
    computed_hmac = hmac.new(key, decrypted_data, hashlib.sha256).hexdigest()

    # Create a response object to send the file with custom headers
    response = send_file(
        io.BytesIO(decrypted_data),
        as_attachment=True,
        download_name=filename
    )
    response.headers['HMAC-Signature'] = computed_hmac
    return response


@app.route('/public_key', methods=['GET'])
def get_public_key():
    return public_key_pem.decode(), 200

if __name__ == '__main__':
    app.run(port=5000)