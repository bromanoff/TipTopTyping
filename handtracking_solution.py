import cv2
import mediapipe as mp
import time
import datetime
from subprocess import call
import numpy as np
from trie import Trie, TrieNode
import math

# TODO: Candidate Selection based on word appearance frequency
# TODO: Backspace, Return and Spacebar

# Palm facing mental model 
CHAR_DICT = {"Left": {
    			0: ["qwert", False],
                1: ["asdf", False],
                2: ["zxc", False],
                3: ["SPACE", False]},
       		"Right": {
             	0: ["yuiop", False],
                1: ["ghjkl", False],
                2: ["vbnm", False],
                3: ["<-", False]}}

# CHAR_DICT = {"Left": {
#     			0: "qaz",
#                 1: "wsx",
#                 2: "edc",
#                 3: "rfvtgb"},
#        		"Right": {
#              	0: "p",
#                 1: "ol",
#                 2: "ik",
#                 3: "yhnujm"}}

#write a list with 10 common known example words
# LANGUAGE = ["hello", "world", "python", "is", "awesome", "language", "programming", "computer", "science", "data", "coverage", "hi"] 
SPRACHE = ["hut", "haus", "haut", "mut", "maus", "maut", "mann", "hello", "world"]  

# Trie Datastruture to store and query language
trie = Trie()
trie.extend(SPRACHE)
                  
#opening camera (0 for the default camera, when iPhone continuity camera is active, it will become the default (0))
videoCap = cv2.VideoCapture(0)
lastFrameTime = 0
frame = 0
handSolution = mp.solutions.hands
hands = handSolution.Hands()

input_msg = []
string_permutations = []
output_msg = ""

def distance(pos1, pos2): #pos = (x, y)
    Distance = int(math.sqrt(((pos2[0] - pos1[0]) * (pos2[0] - pos1[0])) + ((pos2[1] - pos1[1]) * (pos2[1] - pos1[1]))))
    return Distance

def write_char(hand, target):
    global input_msg
    global output_msg
    if not target == 3:
        input_msg.append(CHAR_DICT[hand][target][0])
    else:
        match hand:
            case "Left":
                output_msg += " "
            case "Right":
                output_msg = output_msg[:-1]
        
    CHAR_DICT[hand][target][1] = True
    print(f"Input Message: {input_msg}")
    
    # # print child nodes of current char in trie
    # for char in CHAR_DICT[hand_label][idx]:
    #     print(f"Tree children: {trie.children(char)}")
    
    result = list(trie.complete(input_msg)) # get list of possible words
    if len(result) == 1:    # if there is only one result, autocomplete
        output_msg += result[0] + " "
        print(output_msg)
        input_msg = []
    # time.sleep(0.1)

def char_written(hand, target):
    if CHAR_DICT[hand][target][1] == False:
        return False
    else:
        return True
    
while True:
    frame += 1
    success, img = videoCap.read() #reading image
    # img = cv2.flip(img, 1) #flip image for built in webcam
    # img = cv2.flip(img, 1) #flip image for built in webcam
    
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
        
        for idx in range(len(multi_hand_landmarks_list)):     # for each hand recognized
            hand_landmarks = multi_hand_landmarks_list[idx]   # get the hand landmarks
            handedness = multi_handedness_list[idx]           # get the handedness
            hand_label = handedness.classification[0].label   # get the hand label (left or right)
            
            height, width, _ = img.shape
            # FIXME: Fix thumb position towards tip of thumb
            thumb_pos = (int(hand_landmarks.landmark[4].x * width), int(hand_landmarks.landmark[4].y * height), int(hand_landmarks.landmark[4].z * width))
            # TODO: Create thumb vector from landmark 3 and 4
            pinky_mcp_pos = (int(hand_landmarks.landmark[17].x * width), int(hand_landmarks.landmark[17].y * height))
            
            # # Works only for camera facing perspective
            # if distance(thumb_pos, pinky_mcp_pos) <= 40:
            #     input_msg = []
            #     # print("Input message cleared")
            #     print(hand_label)
            
            # Reset input message when pinky tips touch
            if hand_label == "Left":
                left_pinky_tip_pos = (int(hand_landmarks.landmark[20].x * width), int(hand_landmarks.landmark[20].y * height))
            if hand_label == "Right":
                right_pinky_tip_pos = (int(hand_landmarks.landmark[20].x * width), int(hand_landmarks.landmark[20].y * height))
            
            try: #exception handling for first iteration with uncomputed right pinky tip
                if distance(left_pinky_tip_pos, right_pinky_tip_pos) <= 40:
                    input_msg = []
                    print("Input message cleared")
            except NameError:
                continue
            
            # Thumb Annotations
            cv2.circle(img, (thumb_pos), 5, (0, 255, 0), -1) # Draw Circles on thumb tips
            # cv2.putText(img, hand_label, (thumb_x, thumb_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2) # print only handedness on thumb    
                        
            for idx, point in enumerate(hand_landmarks.landmark[8:21:4]):      # Calculate landmark positions for thumb and finger tips, except pinky [from:to:increment]
                h, w, c = img.shape 
                landmark_pos = (int(point.x * w), int(point.y * h))

                cv2.putText(img, CHAR_DICT[hand_label][idx][0], (landmark_pos), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
                
                # TODO: Add a variable threshold for distance between thumb and finger tips based on possible next characters, PERMUTATIONS?
                # TODO: OR: Only allow characters that are child nodes of chars in input_msg
                # if char in charset and distance <= 90:
                # else …
                # print("distance: ", distance(thumb_pos, landmark_pos))
                # print("char written: ", char_written)
                
                if distance(thumb_pos, landmark_pos) <= 70 and not char_written(hand_label, idx):
                    write_char(hand_label, idx)
                    
                elif distance(thumb_pos, landmark_pos) <= 70 and char_written:
                    pass
                                    
                elif distance(thumb_pos, landmark_pos) > 140 and char_written(hand_label, idx):
                    CHAR_DICT[hand_label][idx][1] = False
                    
    cv2.putText(img, output_msg, (500,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


    cv2.imshow("CamOutput", img)
    cv2.waitKey(1)       
