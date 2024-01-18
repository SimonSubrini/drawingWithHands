import cv2
import mediapipe as mp
from PIL import Image, ImageTk
import tkinter as tk
import imutils
import numpy as np


# Función para obtener las coordenadas de los dedos
def getFingerPosition(landmarks):
    fingers['thumb'] = [landmarks[1], landmarks[2], landmarks[3], landmarks[4]]
    fingers['index'] = [landmarks[6], landmarks[7], landmarks[8]]
    fingers['middle'] = [landmarks[10], landmarks[11], landmarks[12]]
    fingers['ring'] = [landmarks[14], landmarks[15], landmarks[16]]
    fingers['pinky'] = [landmarks[18], landmarks[19], landmarks[20]]
    return fingers


# Función para calcular la distancia entre dos puntos
def dist(point1, point2):
    d = ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5
    return d


# Función para detectar el toque y eliminar puntos
def detectAndEraseTouches(finger_landmarks, points, wrist):
    thumb = finger_landmarks['thumb']
    index = finger_landmarks['index']
    middle = finger_landmarks['middle']
    ring = finger_landmarks['ring']
    pinky = finger_landmarks['pinky']
    thumb_tip = (thumb[3].x * drawWidth, thumb[3].y * drawHeight)  # Obtener las coordenadas x, y del pulgar
    distT_W = dist(thumb_tip, wrist)
    if distT_W > max(dist([index[2].x * drawWidth, index[2].y * drawHeight], wrist),
                     dist([middle[2].x * drawWidth, middle[2].y * drawHeight], wrist),
                     dist([ring[2].x * drawWidth, ring[2].y * drawHeight], wrist),
                     dist([pinky[2].x * drawWidth, pinky[2].y * drawHeight], wrist)):
        thumb_up = True
    else:
        thumb_up = False
    if thumb_up:
        for point in points:
            x, y, _, _ = point
            distance = dist(thumb_tip, (x, y))
            if distance < touch_threshold:
                points.remove(point)
        return True
    return False


# Función para cambiar el tamaño del pincel
def changeBrushSize(finger_landmarks, wrist):
    thumb = finger_landmarks['thumb']
    index = finger_landmarks['index']
    middle = finger_landmarks['middle']
    ring = finger_landmarks['ring']
    pinky = finger_landmarks['pinky']
    thumb_tip = (thumb[3].x * drawWidth, thumb[3].y * drawHeight)  # Obtener las coordenadas x, y del pulgar
    distT_W = dist(thumb_tip, wrist)
    distI_W = dist([index[2].x * drawWidth, index[2].y * drawHeight], wrist)
    distM_W = dist([middle[2].x * drawWidth, middle[2].y * drawHeight], wrist)
    distR_W = dist([ring[2].x * drawWidth, ring[2].y * drawHeight], wrist)
    distP_W = dist([pinky[2].x * drawWidth, pinky[2].y * drawHeight], wrist)
    if distT_W / 1.5 > max(distM_W, distR_W, distP_W) and distI_W > max(distM_W, distR_W, distP_W):
        b_size = int(dist(thumb_tip, (index[2].x * drawWidth, index[2].y * drawHeight)) / 10)
        print(f"brush size: {b_size}")
    else:
        b_size = -1
    return b_size


# Función para agregar puntos en función de otros dedos
def addPointsForFingers(finger_landmarks, s):
    for c, finger in enumerate(finger_landmarks):
        if finger[0].y > finger[1].y > finger[2].y:
            x, y = int(finger[2].x * drawWidth), int(finger[2].y * drawHeight)
            drawn_points.append((x, y, colors[c], s))


def draw_hand(canvas, landmark):
    for fingers_points in landmark:
        canvas.create_oval((fingers_points.x * drawWidth) - 10, (fingers_points.y * drawHeight) - 10,
                           (fingers_points.x * drawWidth) + 10,
                           (fingers_points.y * drawHeight) + 10, fill="#000")

        canvas.create_oval((fingers_points.x * drawWidth) - 5, (fingers_points.y * drawHeight) - 5,
                           (fingers_points.x * drawWidth) + 5,
                           (fingers_points.y * drawHeight) + 5, fill="#fff")


def update_hand_tracking(canvas):
    global drawn_points, brush_size

    ret, frame = cap.read()
    if not ret:
        return

    # ------------------------------------------------------------ Camara
    frame_cam = cv2.resize(frame, (420, 236))
    frame_cam = cv2.flip(frame_cam, 1)
    cam_rgb = cv2.cvtColor(frame_cam, cv2.COLOR_BGR2RGB)
    cam_image = Image.fromarray(cam_rgb)
    cam_image = ImageTk.PhotoImage(image=cam_image)
    lbl_cam.configure(image=cam_image)
    lbl_cam.image = cam_image
    # ------------------------------------------------------------ Dibujo
    frame_draw = cv2.resize(frame, (480, 640))
    frame_draw = cv2.flip(frame_draw, 1)

    frame_rgb = cv2.cvtColor(frame_draw, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    # Limpiar el canvas antes de dibujar
    canvas.delete("all")

    if results.multi_hand_landmarks is not None:
        for hand_landmarks in results.multi_hand_landmarks:
            draw_hand(canvas, hand_landmarks.landmark)

            fingers = getFingerPosition(hand_landmarks.landmark)

            if not detectAndEraseTouches(fingers, drawn_points, (
                    hand_landmarks.landmark[0].x * drawWidth, hand_landmarks.landmark[0].y * drawHeight)):
                s = changeBrushSize(fingers,
                                    (hand_landmarks.landmark[0].x * drawWidth,
                                     hand_landmarks.landmark[0].y * drawHeight))
                if s > 0:
                    brush_size = s
                else:
                    addPointsForFingers([fingers['index'], fingers['middle'], fingers['ring'], fingers['pinky']],
                                        brush_size)

    # Dibujar los puntos en el canvas
    for point in drawn_points:
        x, y, color, size = point
        canvas.create_oval(x - size, y - size, x + size, y + size, fill="#%02x%02x%02x" % color)

    # Llamar a la función nuevamente después de un tiempo
    canvas.after(10, update_hand_tracking, canvas)


def start_frame():
    global cap
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    update_hand_tracking(lbl_draw)


# Funcion finalizar
def stop_frame():
    cap.release()
    cv2.DestroyAllWindows()
    print("FIN")


# ============================================================================================ Main code
# -------------------------------------------------------------------------- Variables mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# -------------------------------------------------------------------------- Variables de dibujo
drawn_points = []
touch_threshold = 40  # Dimensiones del "borrador"
brush_size = 10  # Tamaño del pincel

# Inicialización de diccionario para rastrear los dedos
fingers = {
    'thumb': [],
    'index': [],
    'middle': [],
    'ring': [],
    'pinky': []
}

# Colores
colors = [
    (255, 0, 0), (255, 0, 255), (0, 255, 0), (0, 255, 255)
]

# -------------------------------------------------------------------------- Variables de Tkinter
windowWidth = 1280
windowHeight = 720
camWidth = 420
camHeight = 236
drawWidth = 768
drawHeight = 432

# Crear la ventana principal de Tkinter
window = tk.Tk()
window.geometry("%dx%d" % (window.winfo_screenwidth(), window.winfo_screenheight()))
window.title("DrawingWithHands ")

# Botones
# Iniciar Video
imagenBI = tk.PhotoImage(file="Inicio.png")
inicio = tk.Button(window, text="Iniciar", image=imagenBI, height="40", width="200", command=start_frame)
inicio.place(x=30, y=30)

# Finalizar Video
imagenBF = tk.PhotoImage(file="Finalizar.png")
fin = tk.Button(window, text="Finalizar", image=imagenBF, height="40", width="200", command=stop_frame)
fin.place(x=30, y=100)
# Video
lbl_cam = tk.Label(window)
lbl_cam.place(x=30, y=439)

lbl_draw = tk.Canvas(window, width=drawWidth, height=drawHeight, bg="white")
lbl_draw.place(x=500, y=30)

cap = None

with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.5) as hands:
    # Iniciar el proceso de actualización de la imagen y seguimiento de manos

    window.mainloop()
