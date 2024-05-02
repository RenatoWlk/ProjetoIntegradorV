import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
import json

# CONSTANTES
DADOS_YOLO_PATH = '.././ProjetoIntegradorV/templates/frontend/dados_yolo.json'

AREAS = {
    'area1': [(52,364),(30,417),(73,412),(88,369)],
    'area2': [(105,353),(86,428),(137,427),(146,358)],
    'area3': [(159,354),(150,427),(204,425),(203,353)],
    'area4': [(217,352),(219,422),(273,418),(261,347)],
    'area5': [(274,345),(286,417),(338,415),(321,345)],
    'area6': [(336,343),(357,410),(409,408),(382,340)],
    'area7': [(396,338),(426,404),(479,399),(439,334)],
    'area8': [(458,333),(494,397),(543,390),(495,330)],
    'area9': [(511,327),(557,388),(603,383),(549,324)],
    'area10': [(564,323),(615,381),(654,372),(596,315)],
    'area11': [(616,316),(666,369),(703,363),(642,312)],
    'area12': [(674,311),(730,360),(764,355),(707,308)]
}

# INICIALIZAÇÃO YOLO
model = YOLO('yolov8s.pt')

yolo_data = {area: {"person": 0, "bicycle": 0, "motorcycle": 0, "car": 0, "truck": 0} for area in AREAS}

# PROCESSAR FRAME DO VÍDEO
def process_frame(frame, class_list):
    frame_resized = cv2.resize(frame, (1020, 500))
    results = model.predict(frame_resized)
    detections_df = pd.DataFrame(results[0].boxes.xyxy).astype("float")

    for area_name, area_points in AREAS.items():
        area_detected = False
        for index, row in detections_df.iterrows():
            x1, y1, x2, y2 = map(int, row[:4])
            detection_index = int(row.name)
            detected_class = class_list[detection_index]

            if 'person' in detected_class or 'bicycle' in detected_class or 'motorcycle' in detected_class or 'car' in detected_class or 'truck' in detected_class:
                centerX = (x1 + x2) // 2
                centerY = (y1 + y2) // 2
                results_area = cv2.pointPolygonTest(np.array(area_points, np.int32), ((centerX, centerY)), False)
                if results_area >= 0:
                    cv2.rectangle(frame_resized, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.circle(frame_resized, (centerX, centerY), 3, (0, 0, 255), -1)
                    yolo_data[area_name][detected_class] += 1
                    write_data_json()
                    area_detected = True
        if not area_detected:
            yolo_data[area_name] = {"person": 0, "bicycle": 0, "motorcycle": 0, "car": 0, "truck": 0}
            write_data_json()           
    return frame_resized

# ESCREVER OS DADOS NO JSON
def write_data_json():
    with open(DADOS_YOLO_PATH, 'w') as f:
        json.dump(yolo_data, f)