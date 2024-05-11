from werkzeug.utils import secure_filename  # type: ignore
from flask import Flask, request, jsonify  # type: ignore
from flask_cors import CORS, cross_origin

import subprocess

app = Flask(__name__)
CORS(app)

ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return 'server is live'


@app.route('/process-youtube-link', methods=['POST'])
def process_youtube_link():
    data = request.get_json()
    youtube_link = data.get('youtubeLink')
    process = subprocess.run(['python3', '../whisper.py', youtube_link])
    print(youtube_link, process)
    return jsonify({'message': process.returncode})


@app.route('/process-video-file', methods=['POST'])
def process_youtube_file():
    video_file = request.files['videoFile']

    if video_file and allowed_file(video_file.filename):
        filename = secure_filename(video_file.filename)
        video_file.save(f'uploads/{filename}')  # Save video
        process = subprocess.run(['python3', '../whisper.py', youtube_link])

        print(f"Video saved: {filename}")
        print(
            f"Process text script exited with code: {process.returncode}")
    return jsonify({'message': 'Processing completed!'})


if __name__ == "__main__":
    app.run(debug=True)
