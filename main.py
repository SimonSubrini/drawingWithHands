import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
drawn_points = []
touch_threshold = 40  # Dimensiones del "borrador"

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


# Función para obtener las coordenadas de los dedos
def getFingerPosition(landmarks):
    fingers['thumb'] = [landmarks[1], landmarks[2], landmarks[3], landmarks[4]]
    fingers['index'] = [landmarks[6], landmarks[7], landmarks[8]]
    fingers['middle'] = [landmarks[10], landmarks[11], landmarks[12]]
    fingers['ring'] = [landmarks[14], landmarks[15], landmarks[16]]
    fingers['pinky'] = [landmarks[18], landmarks[19], landmarks[20]]
    return fingers


# Función para detectar el toque y eliminar puntos
def detectAndEraseTouches(hand_landmarks, points):
    thumb = fingers['thumb']
    thumb_tip = hand_landmarks[4]  # Punto de la punta del pulgar
    mean_thumb = (thumb[0].x + thumb[1].x + thumb[2].x + thumb[2].x)/4

    if (thumb[0].x + thumb[3].x)/2 > mean_thumb > (thumb[1].x + thumb[2].x)/2:
        for point in points:
            x, y, _ = point
            distance = ((thumb_tip.x * width - x) ** 2 + (thumb_tip.y * height - y) ** 2) ** 0.5
            if distance < touch_threshold:
                points.remove(point)


# Función para agregar puntos en función de otros dedos
def addPointsForFingers(finger_landmarks):
    for c, finger in enumerate(finger_landmarks):
        if finger[0].y > finger[1].y > finger[2].y:
            x, y = int(finger[2].x * width), int(finger[2].y * height)
            drawn_points.append((x, y, colors[c]))


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

                fingers = getFingerPosition(hand_landmarks.landmark)

                detectAndEraseTouches(hand_landmarks.landmark, drawn_points)

                addPointsForFingers([fingers['index'], fingers['middle'], fingers['ring'], fingers['pinky']])

        # Dibujar todos los puntos almacenados
        for point in drawn_points:
            x, y, color = point
            cv2.circle(frame, (x, y), 10, color, -1)

        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
