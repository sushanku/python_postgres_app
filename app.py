from flask import Flask, request, send_file, jsonify, render_template, redirect, url_for
import psycopg2
import os
from io import BytesIO

app = Flask(__name__)

# Configure Postgres connection using environment variables
conn = psycopg2.connect(
    dbname=os.getenv('POSTGRES_DB'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    host=os.getenv('POSTGRES_HOST'),
    port=os.getenv('POSTGRES_PORT')
)
cursor = conn.cursor()

# Function to create the 'files' table if it doesn't exist
def create_table():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS files (
        id SERIAL PRIMARY KEY,
        filename TEXT NOT NULL,
        data BYTEA NOT NULL,
        mimetype TEXT NOT NULL
    );
    """)
    conn.commit()

# Create the table on app startup
create_table()

# Homepage to upload a file
@app.route('/')
def home():
    return render_template('upload.html')

# File upload functionality
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_data = file.read()
    file_name = file.filename
    file_mimetype = file.content_type

    # Save file to Postgres
    cursor.execute(
        "INSERT INTO files (filename, data, mimetype) VALUES (%s, %s, %s) RETURNING id",
        (file_name, file_data, file_mimetype)
    )
    file_id = cursor.fetchone()[0]
    conn.commit()

    return redirect(url_for('upload_success', file_id=file_id))

# Upload success page
@app.route('/upload_success/<int:file_id>')
def upload_success(file_id):
    return f"File uploaded successfully! File ID: {file_id}"

# Page to list all files and download
@app.route('/download')
def download_page():
    # Fetch all files from Postgres
    cursor.execute("SELECT id, filename FROM files")
    files = cursor.fetchall()

    return render_template('download.html', files=files)

# Route to download file by file ID
@app.route('/download_file/<int:file_id>', methods=['GET'])
def download_file(file_id):
    cursor.execute("SELECT filename, data, mimetype FROM files WHERE id = %s", (file_id,))
    file = cursor.fetchone()

    if file is None:
        return jsonify({"error": "File not found"}), 404

    file_name, file_data, file_mimetype = file
    file_io = BytesIO(file_data)

    # Replace attachment_filename with download_name
    return send_file(file_io, download_name=file_name, mimetype=file_mimetype, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
