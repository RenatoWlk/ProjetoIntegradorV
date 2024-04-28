import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
import json
import time
import threading

yolo_data = {"person": 0, "bicycle": 0, "motorcycle": 0, "car": 0, "truck": 0}

# CONSTANTES
DADOS_YOLO_PATH = '../ProjetoIntegradorV/frontend/dados_yolo.json'
VIDEO_PATH = '../ProjetoIntegradorV/YOLOV8/yolov8parkingspace-main/parking1.mp4'
CLASSES_PATH = '../ProjetoIntegradorV/YOLOV8/yolov8parkingspace-main/classes.txt'
AREA_9 = [(500,327),(550,388),(610,380),(555,324)]

# INICIALIZAÇÃO YOLO
model = YOLO('yolov8s.pt')

# PROCESSAR EVENTOS DO MOUSE
def mouse_event_handler(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:  
        colorsBGR = [x, y]
        print(colorsBGR)

# PROCESSAR FRAME DO VÍDEO
def process_frame(frame, model, class_list):
    frame = cv2.resize(frame, (1020, 500))
    results = model.predict(frame)
    px = pd.DataFrame(results[0].boxes.xyxy).astype("float")
    list9 = []

    for index, row in px.iterrows():
        x1, y1, x2, y2 = map(int, row[:4])
        d = int(row.name)
        c = class_list[d]

        if 'person' in c or 'bicycle' in c or 'motorcycle' in c or 'car' in c or 'truck' in c:
            centerX = (x1 + x2) // 2
            centerY = (y1 + y2) // 2
            results9 = cv2.pointPolygonTest(np.array(AREA_9, np.int32), ((centerX, centerY)), False)
            if results9 >= 0:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.circle(frame, (centerX, centerY), 3, (0, 0, 255), -1)
                list9.append(c)
            yolo_data[c] = len(list9)

    return frame, len(list9)

# DESENHAR ÁREA NO VÍDEO
def draw_area(frame, count):
    if count == 1:
        cv2.polylines(frame, [np.array(AREA_9,np.int32)], True, (0,0,255), 2)
        cv2.putText(frame, str('9'), (591,398), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255), 1)
    else:
        cv2.polylines(frame, [np.array(AREA_9,np.int32)], True, (0,255,0), 2)
        cv2.putText(frame, str('9'), (591,398), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255), 1)

# ESCREVER OS DADOS NO JSON
def write_data_json():
    while True:
        with open(DADOS_YOLO_PATH, 'w') as f:
            json.dump(yolo_data, f)
        time.sleep(1)

# FUNÇÃO PRINCIPAL
def main():
    global yolo_data

    cv2.namedWindow('RGB')
    cv2.setMouseCallback('RGB', mouse_event_handler)

    cap = cv2.VideoCapture(VIDEO_PATH)

    classes_file = open(CLASSES_PATH, "r")
    data = classes_file.read()
    class_list = data.split("\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame, a9 = process_frame(frame, model, class_list)
        draw_area(frame, a9)

        cv2.imshow("RGB", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    thread_write_data = threading.Thread(target=write_data_json)
    thread_write_data.start()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()