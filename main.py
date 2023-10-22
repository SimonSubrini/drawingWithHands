import cv2
import mediapipe as mp
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from threading import Thread
from PIL import Image, ImageTk
import numpy as np

# Set constants
fingers = {
    'thumb': [],
    'index': [],
    'middle': [],
    'ring': [],
    'pinky': []
}

colors = [
    (255, 0, 0), (255, 0, 255), (0, 255, 0), (0, 255, 255)
]

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
width, height = 860, 640

# Declaration of variables
drawn_points = []
touch_threshold = 40
line_width = 10
frame = None


# Declaration of functions
def getFingerPosition(landmarks):
    fingers['thumb'] = [landmarks[1], landmarks[2], landmarks[3], landmarks[4]]
    fingers['index'] = [landmarks[6], landmarks[7], landmarks[8]]
    fingers['middle'] = [landmarks[10], landmarks[11], landmarks[12]]
    fingers['ring'] = [landmarks[14], landmarks[15], landmarks[16]]
    fingers['pinky'] = [landmarks[18], landmarks[19], landmarks[20]]
    return fingers


def detectAndEraseTouches(finger_landmarks, points):
    thumb_tip = fingers['thumb'][3]
    thumb = finger_landmarks['thumb']
    index = finger_landmarks['index']
    middle = finger_landmarks['middle']
    ring = finger_landmarks['ring']
    pinky = finger_landmarks['pinky']
    thumb_up = thumb[3].y < index[2].y and thumb[3].y < middle[2].y and thumb[3].y < ring[2].y and thumb[3].y < pinky[
        2].y
    if thumb_up:
        for point in points:
            x, y, _, _ = point
            distance = ((thumb_tip.x * width - x) ** 2 + (thumb_tip.y * height - y) ** 2) ** 0.5
            if distance < touch_threshold:
                points.remove(point)
        return True
    return False


def addPointsForFingers(finger_landmarks):
    for c, finger in enumerate(finger_landmarks):
        if finger[0].y > finger[1].y > finger[2].y:
            x, y = int(finger[2].x * width), int(finger[2].y * height)
            drawn_points.append((x, y, colors[c], line_width))


def save_image():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        cv2.imwrite(file_path, frame)
        messagebox.showinfo("Guardado", "La imagen se ha guardado exitosamente.")


def change_line_width(val):
    global line_width
    line_width = int(val)


def change_eraser_width(val):
    global touch_threshold
    touch_threshold = int(val)


def update_image():
    global frame
    if frame is not None:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
        label.config(image=photo)
        label.image = photo
        label.after(10, update_image)


def process_images():
    ret = True
    with mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5) as hands:
        while ret:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (width, height))
            frame = cv2.flip(frame, 1)

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            if results.multi_hand_landmarks is not None:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(143, 146, 219), thickness=2, circle_radius=4),
                        mp_drawing.DrawingSpec(color=(179, 208, 65), thickness=4))

                    fingers = getFingerPosition(hand_landmarks.landmark)

                    if not detectAndEraseTouches(fingers, drawn_points):
                        addPointsForFingers([fingers['index'], fingers['middle'], fingers['ring'], fingers['pinky']])

            for point in drawn_points:
                x, y, color, size = point
                cv2.circle(frame, (x, y), size, color, -1)

            cv2.imshow("Frame", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()
    root.quit()  # Detener la GUI al finalizar el procesamiento de imágenes


# GUI elements
root = tk.Tk()
root.title("drawingWithHands")

save_button = tk.Button(root, text="Guardar Imagen", command=save_image)
save_button.pack()

line_width_slider = tk.Scale(root, from_=5, to=25, orient="horizontal", label="Ancho de Línea",
                             command=change_line_width)
line_width_slider.set(10)
line_width_slider.pack()

eraser_width_slider = tk.Scale(root, from_=10, to=20, orient="horizontal", label="Ancho del Borrador",
                               command=change_eraser_width)
eraser_width_slider.set(20)
eraser_width_slider.pack()

label = tk.Label(root)
label.pack()

update_image()
image_thread = Thread(target=process_images)
image_thread.daemon = True
image_thread.start()

root.geometry("900x700")
root.protocol("WM_DELETE_WINDOW", root.quit)  # Manejar el cierre de ventana
root.mainloop()
