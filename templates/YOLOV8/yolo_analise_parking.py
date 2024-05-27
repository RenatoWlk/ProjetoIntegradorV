import cv2
import pandas
import numpy
from ultralytics import YOLO
import json

# CONSTANTES
DADOS_YOLO_PATH = '.././ProjetoIntegradorV/templates/frontend/dados_yolo.json'

# AREAS DO VÍDEO parking1.mp4
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

'''
# AREAS DO VÍDEO estacionamento_video.mp4
AREAS = {
    'area1': [(154,174),(122,220),(210,223),(234,175)],
    'area2': [(233,170),(217,221),(304,216),(313,161)],
    'area3': [(322,158),(310,216),(391,216),(407,161)],
    'area4': [(417,162),(407,216),(486,217),(498,159)],
    'area5': [(504,159),(494,216),(595,217),(606,168)],
    'area6': [(610,156),(604,213),(709,213),(712,157)],
    'area7': [(734,155),(720,209),(801,217),(808,168)],
    'area8': [(58,311), (44,392), (107,392),(143,300)],
    'area9': [(159,301),(127,392),(194,392),(209,301)],
    'area10':[(211,300),(195,393),(259,395),(283,295)],
    'area11':[(291,296),(278,397),(345,395),(353,299)],
    'area12':[(360,296),(352,393),(426,395),(420,293)],
    'area13':[(426,291),(435,392),(506,394),(482,285)],
    'area14':[(490,287),(513,391),(582,393),(545,285)],
    'area15':[(563,314),(603,398),(676,399),(629,306)],
    'area16':[(637,309),(683,397),(756,399),(698,300)],
    'area17':[(705,299),(763,395),(813,370),(769,287)]
}
'''
'''
# AREAS DO VÍDEO estacionamento_enzo.mp4
AREAS = {
    'area1':[(126,219),(175,251),(289,217),(231,192)],
    'area2':[(384,169),(436,155),(488,173),(445,191)],
    'area3':[(292,189),(331,213),(403,192),(362,172)],
    'area4':[(377,271),(459,236),(535,254),(477,300)],
    'area5':[(458,233),(521,202),(586,216),(536,253)],
    'area6':[(176,328),(323,396),(480,305),(365,266)]
}
'''

CONFIDENCE_THRESHOLD = 0.3
FRAME_SIZE = (816, 400)

# INICIALIZAÇÃO YOLO
model = YOLO('yolov8s.pt')

# PROCESSAR FRAME DO VÍDEO
def process_frame(frame, class_list):
    yolo_data = {area: {"bicycle": 0, "motorcycle": 0, "car": 0, "truck": 0, "occupied": 0} for area in AREAS}
    frame_resized = cv2.resize(frame, FRAME_SIZE)
    results = model.predict(frame_resized)
    detections_classes = numpy.ravel(results[0].boxes.cls).astype("int")
    detections_confidence = numpy.ravel(results[0].boxes.conf).astype("float")
    detections_boxes_xyxy = pandas.DataFrame(results[0].boxes.xyxy).astype("float")

    for area_name, area_points in AREAS.items():
        for index, row in detections_boxes_xyxy.iterrows():
            x1, y1, x2, y2 = map(int, row[:4])
            detection_index = detections_classes[index]
            detected_class = class_list[detection_index]

            if detections_confidence[index] >= CONFIDENCE_THRESHOLD:
                if any(vehicle_type in detected_class for vehicle_type in ['bicycle', 'motorcycle', 'car', 'truck']):
                    update_yolo_data(yolo_data, frame_resized, area_name, area_points, detected_class, (x1, y1), (x2, y2))

    write_data_json(yolo_data)
    return frame_resized

def update_yolo_data(yolo_data, frame_resized, area_name, area_points, detected_class, top_left_xy, bottom_right_xy):
    centerX = (top_left_xy[0] + bottom_right_xy[0]) // 2
    centerY = (top_left_xy[1] + bottom_right_xy[1]) // 2
    results_area = cv2.pointPolygonTest(numpy.array(area_points, numpy.int32), ((centerX, centerY)), False)
    if results_area >= 0:
        cv2.rectangle(frame_resized, top_left_xy, bottom_right_xy, (0, 255, 0), 2)
        cv2.circle(frame_resized, (centerX, centerY), 3, (0, 0, 255), -1)
        yolo_data[area_name][detected_class] = int(results_area)
        yolo_data[area_name]["occupied"] = 1

# DESENHAR ÁREA NO VÍDEO
def draw_area(frame):
    for area_name, area_points in AREAS.items():
        cv2.polylines(frame, [numpy.array(area_points, numpy.int32)], True, (0, 255, 0), 2)
        cv2.putText(frame, area_name, area_points[0], cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

# ESCREVER OS DADOS NO JSON
def write_data_json(yolo_data):
    with open(DADOS_YOLO_PATH, 'w') as f:
        json.dump(yolo_data, f)