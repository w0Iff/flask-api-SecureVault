from flask import Flask, render_template, request, send_file
from cryptography.fernet import Fernet
import os
import uuid

app = Flask(__name__)
key_location = 'key.key'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filename = file.filename

    key = load_key()
    cipher = Fernet(key)

    encrypted_filename = str(uuid.uuid4())
    encrypted_data = cipher.encrypt(file.read())

    write_encrypted_file(encrypted_filename, encrypted_data)

    return {"message": "File uploaded and encrypted successfully", "file_id": encrypted_filename}


@app.route('/download/<file_id>')
def download(file_id):
    key = load_key()
    cipher = Fernet(key)

    encrypted_data = read_encrypted_file(file_id)
    decrypted_data = cipher.decrypt(encrypted_data)

    save_decrypted_file(file_id, decrypted_data)

    return send_file(f'tmp/{file_id}', as_attachment=True)


@app.route('/delete/<file_id>', methods=['POST'])
def delete(file_id):
    delete_encrypted_file(file_id)
    delete_decrypted_file(file_id)

    return {"message": "File deleted successfully"}


def load_key():
    if not os.path.exists(key_location):
        generate_key()
    with open(key_location, 'rb') as key_file:
        key = key_file.read()
    return key


def generate_key():
    if not os.path.exists(key_location):
        key = Fernet.generate_key()
        with open(key_location, 'wb') as key_file:
            key_file.write(key)


def read_encrypted_file(file_id):
    with open(f'encrypted_files/{file_id}', 'rb') as enc_file:
        return enc_file.read()


def write_encrypted_file(file_id, data):
    if not os.path.exists('encrypted_files'):
        os.makedirs('encrypted_files')
    with open(f'encrypted_files/{file_id}', 'wb') as enc_file:
        enc_file.write(data)


def save_decrypted_file(file_id, data):
    if not os.path.exists('tmp'):
        os.makedirs('tmp')
    with open(f'tmp/{file_id}', 'wb') as dec_file:
        dec_file.write(data)


def delete_encrypted_file(file_id):
    file_path = f'encrypted_files/{file_id}'
    if os.path.exists(file_path):
        os.remove(file_path)


def delete_decrypted_file(file_id):
    file_path = f'tmp/{file_id}'
    if os.path.exists(file_path):
        os.remove(file_path)


if __name__ == '__main__':
    app.run(debug=True)
