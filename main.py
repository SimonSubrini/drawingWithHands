import cv2
import mediapipe as mp
from PIL import Image, ImageTk, ImageGrab
from tkinter import filedialog, messagebox
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


def changeColor(finger_landmarks, actual_color):
    pinky = finger_landmarks['pinky']
    num_of_px = 845 / len(colors)
    if pinky[2].y * drawHeight < 50:
        actual_color = int(np.round((pinky[2].x * drawWidth) // num_of_px))
        txt_color_option.config(font=("Arial", 50), fg="#%02x%02x%02x" % colors[actual_color])
    return actual_color


# Función para cambiar el tamaño del pincel
def changeBrushSize(finger_landmarks, wrist):
    thumb = finger_landmarks['thumb']
    index = finger_landmarks['index']
    middle = finger_landmarks['middle']
    ring = finger_landmarks['ring']
    pinky = finger_landmarks['pinky']
    thumb_tip = (thumb[3].x * drawWidth, thumb[3].y * drawHeight)  # Obtener las coordenadas x e y del pulgar
    b_size = -1
    if is_finger_up(middle, wrist) and is_finger_up(ring, wrist) and is_finger_up(pinky, wrist):
        b_size = int(dist(thumb_tip, (index[2].x * drawWidth, index[2].y * drawHeight)) / 10)
        txt_size.config(text=f"Tamaño: {b_size}")
    return b_size


def is_finger_up(finger, wrist):
    if dist((finger[2].x * drawWidth, finger[2].y * drawHeight), wrist) > dist(
            (finger[1].x * drawWidth, finger[1].y * drawHeight), wrist) > dist(
        (finger[0].x * drawWidth, finger[0].y * drawHeight), wrist):
        return True
    else:
        return False


# Función para agregar puntos en función de otros dedos
def addPointsForFingers(finger, s, c, wrist):
    if is_finger_up(finger, wrist):
        x, y = int(finger[2].x * drawWidth), int(finger[2].y * drawHeight)
        drawn_points.append((x, y, colors[c], s))


def draw_color_options(canvas):
    for i in range(len(colors)):
        rectangle = canvas.create_rectangle(i * 845 / len(colors), 0, (i + 1) * 845 / len(colors), 50,
                                            fill="#%02x%02x%02x" % colors[i])


def draw_hand(canvas, landmark):
    for fingers_points in landmark:
        canvas.create_oval((fingers_points.x * drawWidth) - 10, (fingers_points.y * drawHeight) - 10,
                           (fingers_points.x * drawWidth) + 10,
                           (fingers_points.y * drawHeight) + 10, fill="#000")

        canvas.create_oval((fingers_points.x * drawWidth) - 5, (fingers_points.y * drawHeight) - 5,
                           (fingers_points.x * drawWidth) + 5,
                           (fingers_points.y * drawHeight) + 5, fill="#808080")
    canvas.create_line((landmark[0].x * drawWidth), (landmark[0].y * drawHeight),
                       (landmark[1].x * drawWidth), (landmark[1].y * drawHeight), fill="#808080", width=4)
    canvas.create_line((landmark[1].x * drawWidth), (landmark[1].y * drawHeight),
                       (landmark[2].x * drawWidth), (landmark[2].y * drawHeight), fill="#808080", width=4)
    canvas.create_line((landmark[2].x * drawWidth), (landmark[2].y * drawHeight),
                       (landmark[3].x * drawWidth), (landmark[3].y * drawHeight), fill="#808080", width=4)
    canvas.create_line((landmark[3].x * drawWidth), (landmark[3].y * drawHeight),
                       (landmark[4].x * drawWidth), (landmark[4].y * drawHeight), fill="#808080", width=4)
    canvas.create_line((landmark[0].x * drawWidth), (landmark[0].y * drawHeight),
                       (landmark[5].x * drawWidth), (landmark[5].y * drawHeight), fill="#808080", width=4)
    canvas.create_line((landmark[0].x * drawWidth), (landmark[0].y * drawHeight),
                       (landmark[17].x * drawWidth), (landmark[17].y * drawHeight), fill="#808080", width=4)

    canvas.create_line((landmark[5].x * drawWidth), (landmark[5].y * drawHeight),
                       (landmark[6].x * drawWidth), (landmark[6].y * drawHeight), fill="#808080", width=4)
    canvas.create_line((landmark[6].x * drawWidth), (landmark[6].y * drawHeight),
                       (landmark[7].x * drawWidth), (landmark[7].y * drawHeight), fill="#808080", width=4)
    canvas.create_line((landmark[7].x * drawWidth), (landmark[7].y * drawHeight),
                       (landmark[8].x * drawWidth), (landmark[8].y * drawHeight), fill="#808080", width=4)

    canvas.create_line((landmark[9].x * drawWidth), (landmark[9].y * drawHeight),
                       (landmark[10].x * drawWidth), (landmark[10].y * drawHeight), fill="#808080", width=4)
    canvas.create_line((landmark[10].x * drawWidth), (landmark[10].y * drawHeight),
                       (landmark[11].x * drawWidth), (landmark[11].y * drawHeight), fill="#808080", width=4)
    canvas.create_line((landmark[11].x * drawWidth), (landmark[11].y * drawHeight),
                       (landmark[12].x * drawWidth), (landmark[12].y * drawHeight), fill="#808080", width=4)

    canvas.create_line((landmark[13].x * drawWidth), (landmark[13].y * drawHeight),
                       (landmark[14].x * drawWidth), (landmark[14].y * drawHeight), fill="#808080", width=4)
    canvas.create_line((landmark[14].x * drawWidth), (landmark[14].y * drawHeight),
                       (landmark[15].x * drawWidth), (landmark[15].y * drawHeight), fill="#808080", width=4)
    canvas.create_line((landmark[15].x * drawWidth), (landmark[15].y * drawHeight),
                       (landmark[16].x * drawWidth), (landmark[16].y * drawHeight), fill="#808080", width=4)

    canvas.create_line((landmark[17].x * drawWidth), (landmark[17].y * drawHeight),
                       (landmark[18].x * drawWidth), (landmark[18].y * drawHeight), fill="#808080", width=4)
    canvas.create_line((landmark[18].x * drawWidth), (landmark[18].y * drawHeight),
                       (landmark[19].x * drawWidth), (landmark[19].y * drawHeight), fill="#808080", width=4)
    canvas.create_line((landmark[19].x * drawWidth), (landmark[19].y * drawHeight),
                       (landmark[20].x * drawWidth), (landmark[20].y * drawHeight), fill="#808080", width=4)

    canvas.create_line((landmark[5].x * drawWidth), (landmark[5].y * drawHeight),
                       (landmark[9].x * drawWidth), (landmark[9].y * drawHeight), fill="#808080", width=4)
    canvas.create_line((landmark[9].x * drawWidth), (landmark[9].y * drawHeight),
                       (landmark[13].x * drawWidth), (landmark[13].y * drawHeight), fill="#808080", width=4)
    canvas.create_line((landmark[13].x * drawWidth), (landmark[13].y * drawHeight),
                       (landmark[17].x * drawWidth), (landmark[17].y * drawHeight), fill="#808080", width=4)


def update_hand_tracking(canvas):
    global drawn_points, brush_size, actual_color

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
    frame_draw = cv2.resize(frame, (640, 480))
    frame_draw = cv2.flip(frame_draw, 1)

    frame_rgb = cv2.cvtColor(frame_draw, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    # Limpiar el canvas antes de dibujar
    canvas.delete("all")

    # Dibujar los puntos en el canvas
    for point in drawn_points:
        x, y, color, size = point
        canvas.create_oval(x - size, y - size, x + size, y + size, fill="#%02x%02x%02x" % color)

    draw_color_options(canvas)

    if results.multi_hand_landmarks is not None:
        for hand_landmarks in results.multi_hand_landmarks:
            draw_hand(canvas, hand_landmarks.landmark)
            wrist = (hand_landmarks.landmark[0].x * drawWidth, hand_landmarks.landmark[0].y * drawHeight)

            fingers = getFingerPosition(hand_landmarks.landmark)

            if not detectAndEraseTouches(fingers, drawn_points, (
                    hand_landmarks.landmark[0].x * drawWidth, hand_landmarks.landmark[0].y * drawHeight)):
                s = changeBrushSize(fingers, wrist)
                actual_color = changeColor(fingers, actual_color)
                if s > 0:
                    brush_size = s
                else:
                    addPointsForFingers(fingers['index'], brush_size, c=actual_color, wrist=wrist)

    # Llamar a la función nuevamente después de un tiempo
    canvas.after(10, update_hand_tracking, canvas)


def start_frame():
    global cap
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    update_hand_tracking(lbl_draw)


def stop_frame():
    global lbl_draw
    cap.release()
    fileLocation = filedialog.asksaveasfilename(defaultextension="jpg")
    x = window.winfo_rootx()
    y = window.winfo_rooty()
    img = ImageGrab.grab(bbox=(x + 485, y + 250, x + 1330, y + 675))

    img.save(fileLocation)
    showImage = messagebox.askyesno("Drawing With Hands", "Do you want to open image?")
    if showImage:
        img.show()


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
    (255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 0, 255), (255, 255, 0), (151, 104, 2), (10, 100, 10),
    (0, 0, 0)
]
actual_color = 0

# -------------------------------------------------------------------------- Variables de Tkinter
windowWidth = 1280
windowHeight = 720
camWidth = 420
camHeight = 236
drawWidth = 845
drawHeight = 475

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
lbl_draw.place(x=485, y=200)
draw_color_options(lbl_draw)

txt_color = tk.Label(window, text="Color: ")
txt_color.config(font=("Arial", 30))
txt_color.place(x=485, y=30)

txt_color_option = tk.Label(window, text=" ■ ")
txt_color_option.config(font=("Arial", 50), fg="#%02x%02x%02x" % colors[actual_color])
txt_color_option.place(x=590, y=10)

txt_size = tk.Label(window, text="Tamaño: 10")
txt_size.config(font=("Arial", 30))
txt_size.place(x=485, y=90)

cap = None

with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.5) as hands:
    window.mainloop()
