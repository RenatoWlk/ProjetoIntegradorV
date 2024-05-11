import cv2
import pandas
import numpy
from ultralytics import YOLO
import json

yolo_data = {"person": 0, "bicycle": 0, "motorcycle": 0, "car": 0, "truck": 0}

# CONSTANTES
DADOS_YOLO_PATH = '.././ProjetoIntegradorV/templates/frontend/dados_yolo.json'
AREA_9 = [(500,327),(550,388),(610,380),(555,324)]

# INICIALIZAÇÃO YOLO
model = YOLO('yolov8s.pt')

# PROCESSAR FRAME DO VÍDEO
def process_frame(frame, class_list):
    global yolo_data
    frame_resized = cv2.resize(frame, (1020, 500))
    results = model.predict(frame_resized)
    detections_classes = numpy.ravel(results[0].boxes.cls).astype("int")
    detections_confidence = numpy.ravel(results[0].boxes.conf).astype("float")
    detections_boxes_xy = pandas.DataFrame(results[0].boxes.xyxy).astype("float")
    area_detected = False

    for index, row in detections_boxes_xy.iterrows():
        x1, y1, x2, y2 = map(int, row[:4])
        detection_index = detections_classes[index]
        detected_class = class_list[detection_index]

        if detections_confidence[index] > 0.60:
            if 'person' in detected_class or 'bicycle' in detected_class or 'motorcycle' in detected_class or 'car' in detected_class or 'truck' in detected_class:
                centerX = (x1 + x2) // 2
                centerY = (y1 + y2) // 2
                results9 = cv2.pointPolygonTest(numpy.array(AREA_9, numpy.int32), ((centerX, centerY)), False)
                if results9 >= 0:
                    cv2.rectangle(frame_resized, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.circle(frame_resized, (centerX, centerY), 3, (0, 0, 255), -1)
                    yolo_data[detected_class] = results9
                    area_detected = True
            write_data_json()
    if not area_detected:
        yolo_data = {"person": 0, "bicycle": 0, "motorcycle": 0, "car": 0, "truck": 0}
        write_data_json() 
    return frame_resized

# DESENHAR ÁREA NO VÍDEO
def draw_area(frame):
    cv2.polylines(frame, [numpy.array(AREA_9,numpy.int32)], True, (0,0,255), 2)
    cv2.putText(frame, str('9'), (591,398), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255), 1)

# ESCREVER OS DADOS NO JSON
def write_data_json():
    with open(DADOS_YOLO_PATH, 'w') as f:
        json.dump(yolo_data, f)

'''
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

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
'''