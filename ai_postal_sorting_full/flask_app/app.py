
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from utils import extract_text_and_pin, assign_bin, log_to_db, notify_robot

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if 'image' not in request.files:
        return 'No file part', 400
    file = request.files['image']
    if file.filename == '':
        return 'No selected file', 400
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    text, pin = extract_text_and_pin(filepath)
    bin_name = assign_bin(pin)
    log_to_db(text, pin, bin_name)
    # Send to ROS bridge
    notify_robot(pin, bin_name)

    return render_template('result.html', text=text, pin=pin, bin=bin_name)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
