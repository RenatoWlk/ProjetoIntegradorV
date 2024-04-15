import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO

# CONSTANTES
VIDEO_PATH = 'D:/Documents/ProjetoIntegradorV/YOLOV8/yolov8parkingspace-main/parking1.mp4'
CLASSES_PATH = 'D:/Documents/ProjetoIntegradorV/YOLOV8/yolov8parkingspace-main/classes.txt'

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

# PROCESSAR EVENTOS DO MOUSE
def mouse_event_handler(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:  
        colorsBGR = [x, y]
        print(colorsBGR)

# FUNÇÃO PRINCIPAL
def main():
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

        frame = cv2.resize(frame, (1020,500))

        results = model.predict(frame)
        #print(results)
        a = results[0].boxes.xyxy
        #print(a)
        px = pd.DataFrame(a).astype("float")
        #print(px)

        occupied_areas = []

        for area_name, area_coords in AREAS.items():
            area_occupied = False
            for index, row in px.iterrows():
                print(f"\nRow: {index}")
                print(row)

                x1 = int(row[0])
                y1 = int(row[1])
                x2 = int(row[2])
                y2 = int(row[3])
                d = int(row.name)
                c = class_list[d]

                if 'car' in c:
                    cx = int(x1+x2) // 2
                    cy = int(y1+y2) // 2

                    results_area = cv2.pointPolygonTest(np.array(area_coords, np.int32), ((cx,cy)), False)
                    if results_area >= 0:
                        cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
                        cv2.circle(frame, (cx,cy), 3, (0,0,255), -1)
                        area_occupied = True

            if area_occupied:
                occupied_areas.append(area_name)

        for area_name, area_coords in AREAS.items():
            if area_name in occupied_areas:
                cv2.polylines(frame, [np.array(area_coords,np.int32)], True, (0,0,255), 2)
                cv2.putText(frame, str(area_name), (area_coords[0][0], area_coords[0][1]), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255), 1)
            else:
                cv2.polylines(frame, [np.array(area_coords,np.int32)], True, (0,255,0), 2)
                cv2.putText(frame, str(area_name), (area_coords[0][0], area_coords[0][1]), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255), 1)

        cv2.imshow("RGB", frame)

        if cv2.waitKey(1)&0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
