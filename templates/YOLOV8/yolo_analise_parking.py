import cv2
import pandas
import numpy
from ultralytics import YOLO
import json

# CONSTANTES
DADOS_YOLO_PATH = '.././ProjetoIntegradorV/templates/frontend/dados_yolo.json'

'''
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
AREAS = {
    'area1': [(82, 215), (195, 194), (255, 195), (143, 221)],
    'area2': [(139, 222), (278, 191), (348, 193), (250, 219)],
    'area3': [(252, 219), (358, 189), (440, 193), (353, 218)],
    'area4': [(355, 218), (445, 190), (538, 188), (460, 215)],
    'area5': [(461, 215), (544, 189), (630, 190), (564, 219)],
    'area6': [(570, 217), (632, 189), (725, 192), (676, 220)],
    'area7': [(681, 214), (728, 191), (813, 186), (793, 212)],
    'area8': [(10, 398), (77, 333), (144, 332), (90, 397)],
    'area9': [(90, 397), (145, 330), (209, 330), (170, 397)],
    'area10': [(170, 398), (207, 330), (278, 329), (251, 397)],
    'area11': [(251, 396), (278, 326), (343, 328), (333, 396)],
    'area12': [(333, 397), (345, 327), (410, 325), (415, 395)],
    'area13': [(414, 397), (409, 326), (477, 326), (498, 398)],
    'area14': [(495, 398), (477, 326), (543, 328), (577, 399)],
    'area15': [(579, 398), (542, 329), (610, 327), (659, 399)],
    'area16': [(662, 398), (610, 326), (675, 329), (738, 398)],
    'area17': [(738, 398), (675, 329), (750, 326), (815, 394)],
}

CONFIDENCE_THRESHOLD = 0.1
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