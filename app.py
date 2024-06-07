from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os
import script  # contains pre-trained model that can detect images

app = Flask(__name__)

googleImages = "https://www.google.com/search?tbm=isch&q="
def imageResultLinks():
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], "image")
    results = script.getPrediction(image_path)
    return [(result, googleImages + result) for result in results]

# Configuration
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename("image")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        prediction_links = imageResultLinks()
        return render_template('upload.html', filename=filename, prediction_links=prediction_links)
    return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=False)