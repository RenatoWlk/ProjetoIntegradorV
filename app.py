# pip install flask
# flask run
import cv2
import json
from flask import Flask, render_template, jsonify, Response
from templates.YOLOV8 import basic, testcount

DADOS_YOLO_PATH = "../ProjetoIntegradorV/templates/frontend/dados_yolo.json"
VIDEO_PATH = '../ProjetoIntegradorV/static/videos/parking1.mp4'
CLASSES_PATH = '../ProjetoIntegradorV/templates/YOLOV8/classes.txt'

app = Flask(__name__)

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
    video = cv2.VideoCapture(VIDEO_PATH)

    while True:
        ret, frame = video.read()
        if not ret:
            break

        classes_file = open(CLASSES_PATH, "r")
        class_list_str = classes_file.read().split("\n")

        # processed_frame = basic.process_frame(frame, class_list_str)
        processed_frame = testcount.process_frame(frame, class_list_str)
        
        _, jpeg = cv2.imencode('.jpg', processed_frame)
        frame_bytes = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    video.release()

@app.route('/video_feed')
def video_feed():
    return Response(process_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)