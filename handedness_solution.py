import cv2
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
import time
import datetime
from subprocess import call
import numpy as np
# from trie import Trie
from trie import Trie, TrieNode
import keyboard

# TODO: Candidate Selection based on word appearance frequency
# TODO: Backspace, Return and Spacebar

THUMB_IDX = 4

FINGER_TIPS = {"INDEX_FINGER_IDX": 8,
                  "MIDDLE_FINGER_IDX": 12,
                  "RING_FINGER_IDX": 16,
                  "PINKY_IDX": 20,}

# # Dictionary to store finger tip values and their corresponding characters
# TIPS = {"left": {"INDEX_FINGER_IDX": [8, "qaz"],
#                   "MIDDLE_FINGER_IDX": [12, "wsx"],
#                   "RING_FINGER_IDX": [16,"edc"],
#                   "PINKY_IDX": [20,"rfvtgb"]},
#         "right": {"INDEX_FINGER_IDX": [8, "p"],
#                   "MIDDLE_FINGER_IDX": [12, "ol"],
#                   "RING_FINGER_IDX": [16,"ik"],
#                   "PINKY_IDX": [20,"yhnujm"]}}

CHAR_DICTX = {"Left": {"INDEX_FINGER_IDX": "qaz",
                  "MIDDLE_FINGER_IDX": "wsx",
                  "RING_FINGER_IDX": "edc",
                  "PINKY_IDX": "rfvtgb"},
        "Right": {"INDEX_FINGER_IDX": "p",
                  "MIDDLE_FINGER_IDX": "ol",
                  "RING_FINGER_IDX": "ik",
                  "PINKY_IDX": "yhnujm"}}

CHAR_DICT = {"INDEX_FINGER_IDX": "abc",
                  "MIDDLE_FINGER_IDX": "def",
                  "RING_FINGER_IDX": "ghi",
                  "PINKY_IDX": "jkl",}

#write a list with 10 common known example words
LANGUAGE = ["hello", "world", "python", "is", "awesome", "language", "programming", "computer", "science", "data", "coverage", "hi"]   

# Trie Datastruture to store and query language
trie = Trie()
trie.extend(LANGUAGE)
                  
#opening camera (0 for the default camera)
videoCap = cv2.VideoCapture(0)
lastFrameTime = 0
frame = 0

# TODO: Check outcome of holistic vs hands
handSolution = mp.solutions.hands
hands = handSolution.Hands()
# handSolution = mp.solutions.holistic
# hands = handSolution.Holistic()

global input_msg
input_msg = []

while True:
    frame += 1
    success, img = videoCap.read() #reading image
    
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #showing image on separate window (only if read was successfull)
    
    #fps calculations
    thisFrameTime = time.time()
    fps = 1 / (thisFrameTime - lastFrameTime)
    lastFrameTime = thisFrameTime
    #write on image fps
    cv2.putText(img, f'FPS:{int(fps)}',
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    #recognize hands from out image
    recHands = hands.process(img)
    multi_hand_landmarks_list = recHands.multi_hand_landmarks
    multi_handedness_list = recHands.multi_handedness
    
    
    if recHands.multi_hand_landmarks:   # if there are any hands recognized
        
        for idx in range(len(multi_hand_landmarks_list)):   # for each hand recognized
            hand_landmarks = multi_hand_landmarks_list[idx]   # get the hand landmarks
            handedness = multi_handedness_list[idx]           # get the handedness
                        
            for datapoint_id, point in enumerate(hand_landmarks.landmark[4:21:4]):
                h, w, c = img.shape 
                x, y = int(point.x * w), int(point.y * h)
                    
                # cv2.circle(img, (x, y), 5, (0, 255, 0), -1) # Draw Circles on Tips
                

            height, width, _ = img.shape
            thumb_x = int(hand_landmarks.landmark[4].x * width)
            thumb_y = int(hand_landmarks.landmark[4].x * height)
            # print(handedness)
            
            hand_label = handedness.classification[0].label
            
            cv2.putText(img, hand_label, (thumb_x, thumb_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2) # print only handedness on thumb                     
            # print(handedness.classification[0].label)


    cv2.imshow("CamOutput", img)
    cv2.waitKey(1)