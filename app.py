from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    files = []
    for root, dirs, filenames in os.walk(app.config['UPLOAD_FOLDER']):
        for fname in filenames:
            full_path = os.path.join(root, fname)
            relative_path = os.path.relpath(full_path, app.config['UPLOAD_FOLDER'])
            files.append(relative_path)
    return render_template('index.html', files=files)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        staff_name = request.form['staff_name']
        doc_type = request.form['doc_type']
        expiry_date = request.form['expiry_date']
        file = request.files['file']

        folder_path = os.path.join(app.config['UPLOAD_FOLDER'], doc_type.replace(' ', '_'))
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        if file and allowed_file(file.filename):
            filename = f"{staff_name}_{expiry_date}_{file.filename}"
            file.save(os.path.join(folder_path, filename))
            return redirect(url_for('index'))
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)