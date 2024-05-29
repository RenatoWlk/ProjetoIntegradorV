from datetime import datetime, timezone
import os
import cv2
import json
from flask import Flask, render_template, jsonify, Response, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from templates.YOLOV8 import basic, yolo_analise_parking

DADOS_YOLO_PATH = "../ProjetoIntegradorV/templates/frontend/dados_yolo.json"
UPLOAD_FOLDER = '../ProjetoIntegradorV/static/videos'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}
CLASSES_PATH = '../ProjetoIntegradorV/templates/YOLOV8/classes.txt'
video_path = '../ProjetoIntegradorV/static/videos/estacionamento_puc.mp4'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ParkingOccupancy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc).replace(tzinfo=None))
    occupied_spaces = db.Column(db.Integer)

with app.app_context():
    db.create_all()

def register_data(occupied_count):
    occupancy_record = ParkingOccupancy(
        occupied_spaces=occupied_count,
    )
    db.session.add(occupancy_record)
    db.session.commit()

@app.route('/')
def index():
    return render_template("frontend/tela.html")

@app.route('/dados_yolo')
def dados_yolo():
    with open(DADOS_YOLO_PATH) as f:
        yolo_data = json.load(f)
    return jsonify(yolo_data)

@app.route('/process_video', methods=['POST'])
def process_video():
    intervalo_segundos = 5
    frame_count = 0
    with open(CLASSES_PATH, "r") as classes_file:
        class_list_str = classes_file.read().split("\n")

    while True:
        video = cv2.VideoCapture(video_path)
        ret = True

        while ret:
            ret, frame = video.read()
            if not ret:
                break

            processed_frame, qtdOccupied = yolo_analise_parking.process_frame(frame, class_list_str)
            
            _, jpeg = cv2.imencode('.jpg', processed_frame)
            frame_bytes = jpeg.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
            frame_count += 1
            
            if frame_count >= intervalo_segundos * 30:
                with app.app_context():
                    register_data(qtdOccupied)
                frame_count = 0

        video.release()

@app.route('/video_feed')
def video_feed():
    return Response(process_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_video', methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            global video_path
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            return redirect(url_for('index'))
    return render_template('frontend/tela.html')

@app.route('/occupancy')
def get_occupancy_data():
    records = ParkingOccupancy.query.order_by(ParkingOccupancy.timestamp).all()
    data = {
        'timestamps': [record.timestamp for record in records],
        'occupied_spaces': [record.occupied_spaces for record in records],
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)