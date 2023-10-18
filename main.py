import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
drawn_points = []
touch_threshold = 40  # Dimensiones del "borrador"
fingers = {
    'thumb': [],
    'index': [],
    'middle': [],
    'ring': [],
    'pinky': []
}


def getFingerPosition(landmarks):
    fingers['thumb'] = [
        landmarks[2],
        landmarks[3],
        landmarks[4]
    ]
    fingers['index'] = [
        landmarks[6],
        landmarks[7],
        landmarks[8]
    ]
    fingers['middle'] = [
        landmarks[10],
        landmarks[11],
        landmarks[12]
    ]
    fingers['ring'] = [
        landmarks[14],
        landmarks[15],
        landmarks[16]
    ]
    fingers['pinky'] = [
        landmarks[18],
        landmarks[19],
        landmarks[20]
    ]
    return fingers


with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.5) as hands:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (860, 640))
        frame = cv2.flip(frame, 1)
        height, width, _ = frame.shape

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks is not None:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(143, 146, 219), thickness=2, circle_radius=4),
                    mp_drawing.DrawingSpec(color=(179, 208, 65), thickness=4))

                fingers = getFingerPosition(hand_landmarks.landmark)  # Obtener las coordenadas de cada punto

                if np.abs(fingers['thumb'][0].y - fingers['thumb'][1].y) < np.abs(
                        fingers['thumb'][1].y - fingers['thumb'][2].y):
                    xT, yT = int(fingers['thumb'][2].x * width), int(fingers['thumb'][2].y * height)
                    for point in drawn_points:
                        x, y, _ = point
                        distance = ((xT - x) ** 2 + (yT - y) ** 2) ** 0.5
                        if distance < touch_threshold:
                            drawn_points.remove(point)
                else:
                    if fingers['index'][0].y > fingers['index'][1].y > fingers['index'][2].y:
                        x, y = int(fingers['index'][2].x * width), int(fingers['index'][2].y * height)
                        color = (0, 0, 255)
                        drawn_points.append((x, y, color))
                    if fingers['middle'][0].y > fingers['middle'][1].y > fingers['middle'][2].y:
                        x, y = int(fingers['middle'][2].x * width), int(fingers['middle'][2].y * height)
                        color = (255, 0, 255)
                        drawn_points.append((x, y, color))
                    if fingers['ring'][0].y > fingers['ring'][1].y > fingers['ring'][2].y:
                        x, y = int(fingers['ring'][2].x * width), int(fingers['ring'][2].y * height)
                        color = (0, 255, 255)
                        drawn_points.append((x, y, color))
                    if fingers['pinky'][0].y > fingers['pinky'][1].y > fingers['pinky'][2].y:
                        x, y = int(fingers['pinky'][2].x * width), int(fingers['pinky'][2].y * height)
                        color = (0, 255, 0)
                        drawn_points.append((x, y, color))

        # Dibujar todos los puntos almacenados
        for point in drawn_points:
            x, y, color = point
            cv2.circle(frame, (x, y), 10, color, -1)

        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
