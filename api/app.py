from werkzeug.utils import secure_filename  # type: ignore
from flask import Flask, request  # type: ignore
import subprocess

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return 'server is live'


@app.route('/video-link', methods=['POST'])
def receive_text():
  if request.method == 'POST':
    text = request.form['text']  # Access text field data

    # Check if video file is present
    video_file = request.files.get('video')  # Using get() to handle optional video

    if video_file and allowed_file(video_file.filename):
      filename = secure_filename(video_file.filename)
      video_file.save(f'uploads/{filename}')  # Save video
      print(f"Video saved: {filename}")
    else:
      print("No video file uploaded")

    print(f"Received text: {text}")
    process = subprocess.run(['python3', '../whisper.py', text])
    print(
        f"Process text script exited with code: {process.returncode}")
    return "Text received successfully!", 200
  else:
    return "Only POST requests allowed", 405

if __name__ == "__main__":
    app.run(debug=True)
