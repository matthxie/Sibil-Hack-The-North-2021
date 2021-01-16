import cv2
import mediapipe as mp
import pyautogui

mouse = pyautogui

x, y = pyautogui.size()



mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
# For webcam input:
hands = mp_hands.Hands(
    min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2)
cap = cv2.VideoCapture(0)
while cap.isOpened():
  width  = x#cap.get(3) # float
  height = y#cap.get(4)
  success, image = cap.read()
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
    if(results.multi_handedness[0].classification[0].label == "Left"):
        right = 0
        left = 1
    if(results.multi_handedness[0].classification[0].label == "Right"):
        right = 1
        left = 0
    for hand_landmarks in results.multi_hand_landmarks:
      counter = counter + 1
      #if(len(results.multi_handedness) > 1):
        #temp2 = results.multi_handedness[1]
        #if(temp2.classification[0].label == "Left"):
          #print("STONKS")
          #print(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width)
         #         
      #if(temp.classification[0].label == "Right"):
       # print("GOTTEM")
        #print(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width)
      if(counter%2==right):
        mouse.moveTo(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width, hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height, _pause = False)
      mp_drawing.draw_landmarks(
          image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
  cv2.imshow('MediaPipe Hands', image)
  if cv2.waitKey(5) & 0xFF == 27:
    break
hands.close()
cap.release()
