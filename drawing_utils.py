# drawing_utils.py
import cv2
import mediapipe as mp
import numpy as np


def getFingerPosition(landmarks):
    fingers = {
        'thumb': [landmarks[1], landmarks[2], landmarks[3], landmarks[4]],
        'index': [landmarks[6], landmarks[7], landmarks[8]],
        'middle': [landmarks[10], landmarks[11], landmarks[12]],
        'ring': [landmarks[14], landmarks[15], landmarks[16]],
        'pinky': [landmarks[18], landmarks[19], landmarks[20]]
    }
    return fingers


def dist(point1, point2):
    d = ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5
    return d


def is_finger_up(finger, wrist):
    if dist((finger[2].x, finger[2].y), wrist) > dist((finger[1].x, finger[1].y), wrist) > dist(
            (finger[0].x, finger[0].y), wrist):
        return True
    else:
        return False
