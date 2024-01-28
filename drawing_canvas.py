# drawing_canvas.py
import tkinter as tk
import cv2
import mediapipe as mp
from PIL import Image, ImageTk, ImageGrab
from drawing_utils import *


def draw_hand(canvas, landmark, drawWidth, drawHeight):
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


def draw_color_options(canvas, colors):
    for i in range(len(colors)):
        canvas.create_rectangle(i * 845 / len(colors), 0, (i + 1) * 845 / len(colors), 50,
                                fill="#%02x%02x%02x" % colors[i])


def update_hand_tracking(hands, canvas, cap, lbl_cam, drawn_points, brush_size, colors, actual_color, drawWidth,
                         drawHeight, touch_threshold, txt_size, txt_color_option):
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
        canvas.create_oval(x - size, y - size, x + size, y + size, fill="#%02x%02x%02x" % color, outline='')

    draw_color_options(canvas, colors)

    if results.multi_hand_landmarks is not None:
        for hand_landmarks in results.multi_hand_landmarks:
            draw_hand(canvas, hand_landmarks.landmark, drawWidth, drawHeight)
            wrist = (hand_landmarks.landmark[0].x * drawWidth, hand_landmarks.landmark[0].y * drawHeight)

            fingers = getFingerPosition(hand_landmarks.landmark)

            if not detectAndEraseTouches(fingers, drawn_points, (
                    hand_landmarks.landmark[0].x * drawWidth, hand_landmarks.landmark[0].y * drawHeight), drawWidth,
                                         drawHeight, touch_threshold):
                s = changeBrushSize(fingers, wrist, drawWidth, drawHeight, txt_size)
                actual_color = changeColor(fingers, actual_color, drawWidth, drawHeight, colors, txt_color_option)
                if s > 0:
                    brush_size = s
                else:
                    thumb = fingers['thumb']
                    index = fingers['index']
                    middle = fingers['middle']
                    if not (is_finger_up(middle, wrist) and is_finger_up(thumb, wrist)):
                        addPointsForFingers(index, brush_size, actual_color, wrist, drawWidth, drawHeight,
                                            colors, drawn_points)

    # Llamar a la función nuevamente después de un tiempo
    canvas.after(10, lambda: update_hand_tracking(hands, canvas, cap, lbl_cam, drawn_points, brush_size, colors,
                                                  actual_color, drawWidth, drawHeight, touch_threshold, txt_size,
                                                  txt_color_option))
    return drawn_points


# Función para detectar el toque y eliminar puntos
def detectAndEraseTouches(finger_landmarks, points, wrist, drawWidth, drawHeight, touch_threshold):
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


def changeColor(finger_landmarks, actual_color, drawWidth, drawHeight, colors, txt_color_option):
    pinky = finger_landmarks['pinky']
    num_of_px = 845 / len(colors)
    if pinky[2].y * drawHeight < 50:
        try:
            actual_color = int(np.round((pinky[2].x * drawWidth) // num_of_px))
            txt_color_option.config(font=("Arial", 50), fg="#%02x%02x%02x" % colors[actual_color])
        except Exception:
            actual_color = len(colors) - 1
            txt_color_option.config(font=("Arial", 50), fg="#%02x%02x%02x" % colors[actual_color])
    return actual_color


# Función para cambiar el tamaño del pincel
def changeBrushSize(finger_landmarks, wrist, drawWidth, drawHeight, txt_size):
    thumb = finger_landmarks['thumb']
    index = finger_landmarks['index']
    middle = finger_landmarks['middle']
    ring = finger_landmarks['ring']
    pinky = finger_landmarks['pinky']
    thumb_tip = (thumb[3].x * drawWidth, thumb[3].y * drawHeight)  # Obtener las coordenadas x e y del pulgar
    b_size = -1
    if is_finger_up(middle, wrist) and is_finger_up(ring, wrist) and not is_finger_up(pinky, wrist):
        b_size = int(dist(thumb_tip, (index[2].x * drawWidth, index[2].y * drawHeight)) / 10)
        txt_size.config(text=f"Tamaño: {b_size}")
    return b_size


def clear_canvas(drawn_points):
    # Borra todos los puntos dibujados
    drawn_points.clear()


# Función para agregar puntos en función de otros dedos
def addPointsForFingers(finger, s, c, wrist, drawWidth, drawHeight, colors, drawn_points):
    if is_finger_up(finger, wrist):
        x, y = int(finger[2].x * drawWidth), int(finger[2].y * drawHeight)
        drawn_points.append((x, y, colors[c], s))
