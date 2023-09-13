import cv2
import mediapipe as mp
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
INDEX_FINGER_IDX = 8
MIDDLE_FINGER_IDX = 12
RING_FINGER_IDX = 16
PINKY_IDX = 20

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
handSolution = mp.solutions.hands
hands = handSolution.Hands()

global input_msg
input_msg = []
    


while True:
    frame += 1
    #reading image
    success, img = videoCap.read()
    #showing image on separate window (only if read was successfull)
    if success:
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
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
        if recHands.multi_hand_landmarks:
            
                
            for hand in recHands.multi_hand_landmarks: #loop through all the hands
                
                # TODO: Each hand should have its own handedness
                
                # Calculate landmark positions
                for datapoint_id, point in enumerate(hand.landmark[4:21:4]):
                    h, w, c = img.shape 
                    x, y = int(point.x * w), int(point.y * h)
                    
                # Get handedness
                for idx, hand_handedness in enumerate(recHands.multi_handedness):
                    # print(hand_handedness.classification)
                    # print(hand_handedness.classification[0].label)
                    handedness = hand_handedness.classification[0].label
                    
                    thumb_x = int((hand.landmark[THUMB_IDX].x * w))
                    thumb_y = int((hand.landmark[THUMB_IDX].y * h))
                    
                    for finger in FINGER_TIPS:
                        
                        # for finger in TIPS[hand]:
                        finger_y = int((hand.landmark[FINGER_TIPS[finger]].y * h))
                        finger_x = int((hand.landmark[FINGER_TIPS[finger]].x * w))
                        distance = abs(thumb_y - finger_y)
                        
                        """Trying match case statement """  
                        # match handedness:
                        #     case "Left":
                        #         cv2.putText(img, handedness, (thumb_x, thumb_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2) # print only handedness on thumb
                        #     case "Right":
                        #         cv2.putText(img, handedness, (thumb_x, thumb_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2) # print only handedness on thumb
                        #     case _:
                        #         print("No handedness")                          
                            
                        # Draw circles and charset on finger tips
                        cv2.circle(img, (thumb_x, thumb_y), 10, (255, 0, 255), cv2.FILLED)
                        # cv2.putText(img, handedness, (thumb_x, thumb_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2) # print only handedness on thumb
                        # cv2.circle(img, (x, y), 10, (255, 0, 255), cv2.FILLED) # print circle on tips
                        cv2.putText(img, CHAR_DICTX[handedness][finger], (finger_x, finger_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
                        if distance <= 50:
                            # print(CHAR_DICT[finger])
                            input_msg.append(CHAR_DICTX[handedness][finger])
                            print(f"Input Message: {input_msg}")
                            print(handedness)
                            # for i in CHAR_DICT[finger]:
                            #     input_msg.append(i)
                            print(list(trie.complete(input_msg)))
                            time.sleep(0.2)

                        """Trying to fix the problem of the same character being typed multiple times when the distance between the thumb and finger is less than 40"""
                            
                            # # FIXME: Run only once when distance is equal to or less than 40
                            # typed = False
                            # while distance <= 40:
                            #     if not typed:
                            #         # print(CHAR_DICT[finger])
                            #         input_msg.append(CHAR_DICTX[handedness][finger])
                            #         print(f"Input Message: {input_msg}")
                            #         # for i in CHAR_DICT[finger]:
                            #         #     input_msg.append(i)
                            #         print(list(trie.complete(input_msg)))
                            #         typed = True
                            #         # time.sleep(0.1)
                            #     # if distance > 40:
                            #     #     typed = False
                            #     #     break
                            #     break
                
                
                
                # FIXME: Fix handedness problem. Both ahnds are either left or right but not left and right
                
                # if handedness == "Left":
                #     for finger in FINGER_TIPS:
                #     # for finger in TIPS[hand]:
                #         finger_y = int((hand.landmark[FINGER_TIPS[finger]].y * h))
                #         finger_x = int((hand.landmark[FINGER_TIPS[finger]].x * w))
                #         distance = abs(thumb_y - finger_y)
                        
                #         # Draw circles and charset on finger tips
                #         cv2.circle(img, (thumb_x, thumb_y), 10, (255, 0, 255), cv2.FILLED)
                #         cv2.putText(img, CHAR_DICTX["left"][finger], (finger_x, finger_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
                        
                        
                #         if distance <= 40:
                #             # print(CHAR_DICT[finger])
                #             input_msg.append(CHAR_DICTX["left"][finger])
                #             print(f"Input Message: {input_msg}")
                #             # for i in CHAR_DICT[finger]:
                #             #     input_msg.append(i)
                #             print(list(trie.complete(input_msg)))
                #             time.sleep(0.1)
                
                # if handedness == "Right":
                #     for finger in FINGER_TIPS:
                #     # for finger in TIPS[hand]:
                #         finger_y = int((hand.landmark[FINGER_TIPS[finger]].y * h))
                #         finger_x = int((hand.landmark[FINGER_TIPS[finger]].x * w))
                #         distance = abs(thumb_y - finger_y)
                        
                #         # Draw circles and charset on finger tips
                #         cv2.circle(img, (thumb_x, thumb_y), 10, (255, 0, 255), cv2.FILLED)
                #         cv2.putText(img, CHAR_DICTX["right"][finger], (finger_x, finger_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
                        
                        
                #         if distance <= 40:
                #             # print(CHAR_DICT[finger])
                #             input_msg.append(CHAR_DICTX["right"][finger])
                #             print(f"Input Message: {input_msg}")
                #             # for i in CHAR_DICT[finger]:
                #             #     input_msg.append(i)
                #             print(list(trie.complete(input_msg)))
                #             time.sleep(0.1)
                        
                        
                    
                    # # use the keyboard library to listen to a keypress at any time without interrupting the program
                    # if keyboard.is_pressed(1):
                    #     print(input_msg[1])
                    #     input_msg = []
                    #     # print(list(trie.complete(input_msg)))
                    
                    # # Awaiting key presses as candidate selection
                    # event = keyboard.read_event()
                    # if event.event_type == keyboard.KEY_DOWN and event.name == 'q':
                    #     try:
                    #         print(input_msg[1])
                    #     except IndexError:
                    #         pass
                            
                        

        
                    # for key in [1,2,3]:
                    #     if keyboard.is_pressed(key):
                    #         print(input_msg[key])
                        


        cv2.imshow("CamOutput", img)
        cv2.waitKey(1)