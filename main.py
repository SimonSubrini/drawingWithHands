import cv2
import mediapipe as mp
from PIL import Image, ImageTk, ImageGrab
from tkinter import filedialog, messagebox
import tkinter as tk
import numpy as np
from drawing_canvas import *
from drawing_utils import *


def start_frame():
    global cap
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    update_hand_tracking(hands, lbl_draw, cap, lbl_cam, drawn_points, brush_size, colors, actual_color, drawWidth,
                         drawHeight, touch_threshold, txt_size, txt_color_option)


def stop_frame():
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
draw_color_options(lbl_draw, colors)

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
