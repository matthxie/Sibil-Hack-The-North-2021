import cv2
import mediapipe as mp
import pyautogui
import stoptracking

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mouse = pyautogui

width, height = mouse.size()

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

  image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
  
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
  
  if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
      mp_drawing.draw_landmarks(
          image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

      # Index finger tip coordinates.
      indexRX = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x 
      indexRY = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y 
      indexRZ = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].z

      # Thumb tip coords
      thumbRX = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x 
      thumbRY = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y 
      thumbRZ = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].z 

      # Middle tip coords
      middleRX = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x
      middleRY = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y 
      middleRZ = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].z
      
      """
      print(
        f'Index Finger: '
        f'{mouseX}, '
        f'{mouseY}),'
        f'{mouseZ}), '
        '\n'

        f'Thumb: '
        f'{thumbX}, '
        f'{thumbY}),'
        f'{thumbZ})'
        '\n'
      )
      """
      if not stoptracking.stopTracking(indexRY, thumbRY):
        mouse.moveTo(indexRX * width, indexRY  * height, _pause = False)

      
      """
      if thumbX-mouseX < 3 and thumbY-mouseY < 3:
          print("click")
          mouse.mouseDown(button = 'left')
      else
          mouse.mouseUp(button = 'left')

      if mouseX-middleX < 10 and mouseY-middleY < 10:
          print("scroll")
          mouse.scroll(ds)
      """
      
  #cv2.namedWindow('MediaPipe Hands')
  #cv2.moveWindow('MediaPipe Hands', 0,0)
  #cv2.imshow('MediaPipe Hands', image)
  
  if cv2.waitKey(5) & 0xFF == 27:
    break

hands.close()
cap.release()
