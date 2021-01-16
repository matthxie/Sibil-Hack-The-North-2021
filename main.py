import cv2
import mediapipe as mp
import pyautogui
import stoptracking

mouse = pyautogui

width, height = mouse.size()

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
# For webcam input:
hands = mp_hands.Hands(
    min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2)
cap = cv2.VideoCapture(0)
while cap.isOpened():
  success, image = cap.read()
  image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    
  if not success:
    print("Ignoring empty camera frame.")
    continue
  image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
  image.flags.writeable = False
  results = hands.process(image)
  image.flags.writeable = True
  image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

#code starts here
  counter=0
  if results.multi_hand_landmarks: 
    if(results.multi_handedness[0].classification[0].label == "Left"): #if first hand on screen is left, right click is even
        right = 0
        left = 1
    if(results.multi_handedness[0].classification[0].label == "Right"): #if first hand on screen is right, right click is odd
        right = 1
        left = 0
        
    #receive output from model    
    for hand_landmarks in results.multi_hand_landmarks:
      counter = counter + 1
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
    
      #right hand code (every alternate iteration)
      if(counter%2==right):
        if not stoptracking.stopTracking(indexRY, indexRX, thumbRY, thumbRX):
          mouse.moveTo(indexRX * width, indexRY * height, _pause = False)
        
      #left hand code (every alternate iteration)
      if(counter%2==left) :
        if(abs(indexRX-thumbRX) < 0.02 and abs(indexRY-thumbRY) < 0.04):
          mouse.mouseDown(button = 'left')
        else :
          mouse.mouseUp(button = 'left')

        if(abs(middleRX-thumbRX) < 0.02 and abs(middleRY-thumbRY) < 0.04):
          mouse.mouseDown(button = 'right')
        else :
          mouse.mouseUp(button = 'right')
            
      #mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
  
  #cv2.imshow('MediaPipe Hands', image)
  if cv2.waitKey(5) & 0xFF == 27:
    break
  
hands.close()
cap.release()

#if(len(results.multi_handedness) > 1):
        #temp2 = results.multi_handedness[1]
        #if(temp2.classification[0].label == "Left"):
          #print("STONKS")
          #print(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width)
         #         
      #if(temp.classification[0].label == "Right"):
       # print("GOTTEM")
        #print(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width)  
