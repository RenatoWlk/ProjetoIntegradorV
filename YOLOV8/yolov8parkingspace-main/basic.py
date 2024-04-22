import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
import json
import time
import threading

dados_yolo = {"carro": 0}

# CONSTANTES
DADOS_YOLO_PATH = 'D:\\Documents\\ProjetoIntegradorV\\frontend\\dados_yolo.json'
VIDEO_PATH = 'D:/Documents/ProjetoIntegradorV/YOLOV8/yolov8parkingspace-main/parking1.mp4'
CLASSES_PATH = 'D:/Documents/ProjetoIntegradorV/YOLOV8/yolov8parkingspace-main/classes.txt'
AREA_9 = [(500,327),(550,388),(610,380),(555,324)]

# INICIALIZAÇÃO YOLO
model = YOLO('yolov8s.pt')

# PROCESSAR EVENTOS DO MOUSE
def mouse_event_handler(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:  
        colorsBGR = [x, y]
        print(colorsBGR)

def escrever_dados_json():
    while True:
        with open(DADOS_YOLO_PATH, 'w') as f:
            json.dump(dados_yolo, f)
        time.sleep(1)

# FUNÇÃO PRINCIPAL
def main():
    global dados_yolo

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

        list9 = []
    
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

                results9 = cv2.pointPolygonTest(np.array(AREA_9, np.int32), ((cx,cy)), False)
                if results9 >= 0:
                    cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
                    cv2.circle(frame, (cx,cy), 3, (0,0,255), -1)
                    list9.append(c)
            
        a9 = (len(list9))
        dados_yolo["carro"] = a9

        if a9 == 1:
            cv2.polylines(frame, [np.array(AREA_9,np.int32)], True, (0,0,255), 2)
            cv2.putText(frame, str('9'), (591,398), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255), 1)
        else:
            cv2.polylines(frame, [np.array(AREA_9,np.int32)], True, (0,255,0), 2)
            cv2.putText(frame, str('9'), (591,398), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255), 1)

        cv2.imshow("RGB", frame)

        if cv2.waitKey(1)&0xFF == 27:
            break

    thread_escrita_dados = threading.Thread(target=escrever_dados_json)
    thread_escrita_dados.start()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()