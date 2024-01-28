import cv2
import mediapipe as mp
from PIL import Image, ImageTk, ImageGrab
from tkinter import filedialog, messagebox
import tkinter as tk
import numpy as np
from drawing_canvas import *
from drawing_utils import *


def start_frame():
    global cap, drawn_points
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    drawn_points = update_hand_tracking(hands, canvas, cap, lbl_cam, drawn_points, brush_size, colors, actual_color,
                                        drawWidth,
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


def show_instructions():
    instructions_window = instructions_screen(window)


class instructions_screen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Instrucciones")
        self.geometry("800x600")

        tk.Label(self, text="Instrucciones de uso", font=("Arial", 30)).place(x=240, y=30)

        tk.Label(self, text="Posición de la mano:", font=("Arial", 15, "bold"), justify="left").place(x=100, y=90)
        tk.Label(self,
                 text="Asegúrate de que tu mano esté siempre visible y frente a la pantalla para un mejor seguimiento.",
                 font=("Arial", 10), justify="left").place(
            x=140, y=125)

        tk.Label(self, text="Dibujar:", font=("Arial", 15, "bold"), justify="left").place(x=100, y=160)
        tk.Label(self, text="Para dibujar, extiende únicamente tu dedo índice y muévelo sobre la pantalla.",
                 font=("Arial", 10), justify="left").place(
            x=140, y=195)

        tk.Label(self, text="Borrar:", font=("Arial", 15, "bold"), justify="left").place(x=100, y=230)
        tk.Label(self, text="Para borrar, extiende únicamente tu dedo pulgar y deslízalo sobre la pantalla.",
                 font=("Arial", 10), justify="left").place(
            x=140, y=265)

        tk.Label(self, text="Cambiar el Tamaño del Pincel:", font=("Arial", 15, "bold"), justify="left").place(x=100,
                                                                                                               y=300)
        tk.Label(self, text="Abre tu mano y cierra el meñique. Luego, varía la distancia entre el índice y el pulgar.",
                 font=("Arial", 10), justify="left").place(
            x=140, y=335)

        tk.Label(self, text="Cambiar de Color del Pincel:", font=("Arial", 15, "bold"), justify="left").place(x=100,
                                                                                                              y=370)
        tk.Label(self,
                 text="Levanta solo el dedo meñique y selecciona el color deseado deslizando el dedo por el selector.",
                 font=("Arial", 10), justify="left").place(
            x=140, y=405)

        tk.Label(self, text="Guardar:", font=("Arial", 15, "bold"), justify="left").place(x=100,
                                                                                          y=440)
        tk.Label(self,
                 text="Para guardar tu obra de arte, presiona el botón 'Guardar', colocale un nombre y la extensión "
                      "deseada.",
                 font=("Arial", 10), justify="left").place(
            x=140, y=475)


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

# Botón Iniciar
imagenBI = tk.PhotoImage(file="BTN_inicio.png")
inicio = tk.Button(window, text="Iniciar", image=imagenBI, height="80", width="400", command=start_frame,
                   borderwidth=0, highlightthickness=0)
inicio.place(x=30, y=30)

# Botón Finalizar
imagenBF = tk.PhotoImage(file="BTN_guardar.png")
fin = tk.Button(window, text="Finalizar", image=imagenBF, height="80", width="400", command=stop_frame,
                borderwidth=0, highlightthickness=0)
fin.place(x=30, y=130)

# Botón Borrar
imagenBE = tk.PhotoImage(file="BTN_borrar.png")
borrar = tk.Button(window, text="Borrar", image=imagenBE, height="80", width="400",
                   command=lambda: clear_canvas(drawn_points), borderwidth=0, highlightthickness=0)
borrar.place(x=30, y=230)

# Botón Ayuda
imagenBA = tk.PhotoImage(file="BTN_ayuda.png")
ayuda = tk.Button(window, text="Ayuda", image=imagenBA, height="80", width="400",
                  command=show_instructions, borderwidth=0, highlightthickness=0)
ayuda.place(x=30, y=330)

# Video
lbl_cam = tk.Label(window)
lbl_cam.place(x=30, y=439)

canvas = tk.Canvas(window, width=drawWidth, height=drawHeight, bg="white")
canvas.place(x=485, y=200)
draw_color_options(canvas, colors)

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
