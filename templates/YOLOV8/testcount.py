import cv2
import pandas
import numpy
from ultralytics import YOLO
import json

# CONSTANTES
DADOS_YOLO_PATH = '.././ProjetoIntegradorV/templates/frontend/dados_yolo.json'

AREAS = {
    'area1':[(42,291),(24,334),(58,330),(70,295)],
    'area2':[(84,282),(69,342),(110,342),(117,286)],
    'area3':[(127,283),(120,342),(163,340),(162,282)],
    'area4':[(174,282),(175,338),(218,334),(209,278)],
    'area5':[(219,276),(229,334),(270,332),(257,276)],
    'area6':[(269,274),(286,328),(327,326),(306,272)],
    'area7':[(317,270),(341,323),(383,319),(351,267)],
    'area8':[(366,266),(395,318),(434,312),(396,264)],
    'area9':[(409,262),(446,310),(482,306),(439,259)],
    'area10':[(451,258),(492,305),(523,298),(477,252)],
    'area11':[(493,253),(533,295),(562,290),(514,250)],
    'area12':[(539,249),(584,288),(611,284),(566,246)]
}

CONFIDENCE_THRESHOLD = 0.4

# INICIALIZAÇÃO YOLO
model = YOLO('yolov8s.pt')

yolo_data = {area: {"bicycle": 0, "motorcycle": 0, "car": 0, "truck": 0, "occupied": 0} for area in AREAS}

# PROCESSAR FRAME DO VÍDEO
def process_frame(frame, class_list):
    global yolo_data
    frame_resized = cv2.resize(frame, (816, 400))
    results = model.predict(frame_resized)
    detections_classes = numpy.ravel(results[0].boxes.cls).astype("int")
    detections_confidence = numpy.ravel(results[0].boxes.conf).astype("float")
    detections_boxes_xyxy = pandas.DataFrame(results[0].boxes.xyxy).astype("float")
    area_detected = False

    for area_name, area_points in AREAS.items():
        area_detected = False
        for index, row in detections_boxes_xyxy.iterrows():
            x1, y1, x2, y2 = map(int, row[:4])
            detection_index = detections_classes[index]
            detected_class = class_list[detection_index]

            if detections_confidence[index] >= CONFIDENCE_THRESHOLD:
                if 'bicycle' in detected_class or 'motorcycle' in detected_class or 'car' in detected_class or 'truck' in detected_class:
                    centerX = (x1 + x2) // 2
                    centerY = (y1 + y2) // 2
                    results_area = cv2.pointPolygonTest(numpy.array(area_points, numpy.int32), ((centerX, centerY)), False)
                    if results_area >= 0:
                        cv2.rectangle(frame_resized, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.circle(frame_resized, (centerX, centerY), 3, (0, 0, 255), -1)
                        yolo_data[area_name][detected_class] = int(results_area)
                        yolo_data[area_name]["occupied"] = 1
                        area_detected = True
                write_data_json()
        if not area_detected:
            yolo_data[area_name] = {"bicycle": 0, "motorcycle": 0, "car": 0, "truck": 0, "occupied": 0}
            write_data_json()
    return frame_resized

# DESENHAR ÁREA NO VÍDEO
def draw_area(frame):
    for area_name, area_points in AREAS.items():
        cv2.polylines(frame, [numpy.array(area_points, numpy.int32)], True, (0, 255, 0), 2)
        cv2.putText(frame, area_name, area_points[0], cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

# ESCREVER OS DADOS NO JSON
def write_data_json():
    with open(DADOS_YOLO_PATH, 'w') as f:
        json.dump(yolo_data, f)