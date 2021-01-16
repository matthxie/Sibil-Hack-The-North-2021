import cv2
import mediapipe as mp
import pyautogui
import stoptracking
import math

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mouse = pyautogui
stopTracking = stoptracking.stopTracking

width, height = mouse.size()
dim = (width, height)

trackingConfidence = 0.6
detectionConfidence = 0.6

# For webcam input:
hands = mp_hands.Hands(
    min_detection_confidence = detectionConfidence,
    min_tracking_confidence = trackingConfidence)

cap = cv2.VideoCapture(0)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)

while cap.isOpened():
  success, image = cap.read()

  image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
  
  #width  = cap.get(3)
  #height = cap.get(4)
  
  if not success:
    print("Ignoring empty camera frame.")
    
    # If loading a video, use 'break' instead of 'continue'.
    continue

  # Flip the image horizontally for a later selfie-view display, and convert
  # the BGR image to RGB.
  image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
  
  # To improve performance, optionally mark the image as not writeable to
  # pass by reference.
  
  image.flags.writeable = False
  results = hands.process(image)

  # Draw the hand annotations on the image.
  
  image.flags.writeable = True
  image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
  counter=0
  if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
      #mp_drawing.draw_landmarks(
         # image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

      if(results.multi_handedness[0].classification[0].label == "Left"):
        right = 0
        left = 1
      if(results.multi_handedness[0].classification[0].label == "Right"):
        right = 1
        left = 0
      for hand_landmarks in results.multi_hand_landmarks:
        counter = counter + 1
      # Index finger tip coordinates.
      indexX = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x 
      indexY = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y 

      # Thumb tip coords
      thumbX = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x 
      thumbY = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
      
      if(counter%2==right):
        if not stopTracking(indexY, thumbY):
          mouse.moveTo(indexX * width, indexY * height, _pause = False)
        mp_drawing.draw_landmarks(
          image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
      #if(counter%2 == left):
        

      #if not (math.fabs(indexRY - thumbRY) < 0.1):
       # mouse.moveTo(indexRX * width, indexRY  * height, _pause = False)
      
  #cv2.namedWindow('MediaPipe Hands')
  #cv2.moveWindow('MediaPipe Hands', 0,0)
  #cv2.imshow('MediaPipe Hands', image)
  
  if cv2.waitKey(5) & 0xFF == 27:
    break

hands.close()
cap.release()
