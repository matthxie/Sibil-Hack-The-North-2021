import cv2
import mediapipe as mp
import pyautogui
import ctypes
import stoptracking

user32 = ctypes.windll.user32

mouse = pyautogui

width = user32.GetSystemMetrics(0)
height = user32.GetSystemMetrics(1)
dim = (width, height)

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
# For webcam input:
hands = mp_hands.Hands(
    min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=2)
cap = cv2.VideoCapture(0)

#print(*mp_hands.HandLandmark, sep=", ")

while cap.isOpened():
  #width  = user32.GetSystemMetrics(0) # float
  #height = user32.GetSystemMetrics(1)
  #width = cap.get(3)
  #height = cap.get(4)
  success, image = cap.read()
  if not success:
    print("Ignoring empty camera frame.")
    # If loading a video, use 'break' instead of 'continue'.
    continue

  # Flip the image horizontally for a later selfie-view display, and convert
  # the BGR image to RGB.
  image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
  image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
  # To improve performance, optionally mark the image as not writeable to
  # pass by reference.
  image.flags.writeable = False
  results = hands.process(image)

  # Draw the hand annotations on the image.
  image.flags.writeable = True
  image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
  if results.multi_hand_landmarks: 
    for hand_landmarks in results.multi_hand_landmarks:
      indexRx = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
      indexRy = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
      thumbRx = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
      thumbRy = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
      #print("index finger: " + str(indexRx) + ", " + str(indexRy) + "\nthumb: " + str(thumbRx) + ", " + str(thumbRy))
      if not stoptracking.stopTracking(indexRy, thumbRy):
        mouse.moveTo(indexRx * width, indexRy * height, _pause = False)
      mp_drawing.draw_landmarks(
          image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
      
  cv2.imshow('MediaPipe Hands', image)
  if cv2.waitKey(5) & 0xFF == 27:
    break
hands.close()
cap.release()