import cv2

#VIDEO_PATH = './ProjetoIntegradorV/static/videos/estacionamento_video.mp4'
VIDEO_PATH = 'static/videos/estacionamento_puc.mp4'

def get_coordinates_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"({x},{y}),")

def get_video_coordinates(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Erro ao abrir o vídeo")

    frame_number = 100
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    ret, frame = cap.read()
    cap.release()
    
    if not ret or frame is None:
        print("Erro ao ler o quadro do vídeo")
        return

    resized_frame = cv2.resize(frame, (816, 400))

    cv2.namedWindow('Video Frame')
    cv2.setMouseCallback('Video Frame', get_coordinates_click)
    cv2.imshow('Video Frame', resized_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

get_video_coordinates(VIDEO_PATH)