import os
import uuid
from cryptography.fernet import Fernet
from flask import Flask, request, send_file

app = Flask(__name__):
app.debug = True

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    
    unique_filename = str(uuid.uuid4()) + '_' + uploaded_file.filename
    
    encryption_key = Fernet.generate_key()
    cipher_suite = Fernet(encryption_key)
    encrypted_data = cipher_suite.encrypt(uploaded_file.read())
    with open(unique_filename, 'wb') as file:
        file.write(encrypted_data)
    
    return 'Plik zostal pomyslnie przeslany i zaszyfrowany.'

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    with open(filename, 'rb') as file:
        encrypted_data = file.read()

    encryption_key = request.args.get('encryption-key')
    cipher_suite = Fernet(encryption_key)
    decrypted_data = cipher_suite.decrypt(encrypted_data)

    temp_filename = 'temp_' + filename
    with open(temp_filename, 'wb') as file:
        file.write(decrypted_data)

    return send_file(temp_filename, as_attachment=True)


if __name__ == '__main__':
    app.run()
