import cv2
from PIL import ImageFont, ImageDraw, Image  
import mediapipe as mp
import time
import datetime
from subprocess import call
import numpy as np
from trie import Trie, TrieNode
import math
from playsound import playsound

# TODO: Candidate Selection based on word appearance frequency
# TODO: change false character in test phrase to first of input message
# TODO: display first char of entered group as user types
# TODO: display first candidate as word extension 
# TODO: implement candidate selection on space

# Palm facing mental model 
CHAR_DICT = {"Right": {
    			0: ["qwert", False],
                1: ["asdf", False],
                2: ["zxc", False],
                3: ["SPACE", False]},
       		"Left": {
             	0: ["yuiop", False],
                1: ["ghjkl", False],
                2: ["vbnm", False],
                3: ["<-", False]}}

# #allcaps chars
# CHAR_DICT = {"Right": {
#     			0: ["QWERT", False],
#                 1: ["ASDF", False],
#                 2: ["ZXC", False],
#                 3: ["SPACE", False]},
#        		"Left": {
#              	0: ["YUIOP", False],
#                 1: ["GHJKL", False],
#                 2: ["VBNM", False],
#                 3: ["<-", False]}}

LANGUAGE = ["hut", "haus", "haut", "mut", "maus", "maut", "mann", "hello", "world"]  

# pull random phrase from phrases2.txt and save it in a variable
with open("phrases/phrases2.txt", "r") as f:
    phrases = f.readlines()
    test_phrase = phrases[np.random.randint(0, len(phrases))].strip()
    
test_phrase = "hello world"

phrase_chars = {}
for idx, symbol in enumerate(test_phrase):
    phrase_chars[idx] = [idx * 30, symbol, (105, 105, 105)]
    
# Trie Datastruture to store and query language
trie = Trie()
trie.extend(LANGUAGE)
                  
#opening camera (0 for the default camera, when iPhone continuity camera is active, it will become the default (0))
videoCap = cv2.VideoCapture(0)
lastFrameTime = 0
frame = 0
handSolution = mp.solutions.hands
hands = handSolution.Hands()

input_msg = []
output_msg = ""

line_pos_x = [400, 430]

def distance(pos1, pos2): #pos = (x, y)
    Distance = int(math.sqrt(((pos2[0] - pos1[0]) * (pos2[0] - pos1[0])) + ((pos2[1] - pos1[1]) * (pos2[1] - pos1[1]))))
    return Distance

def write_char(hand, target):
    global input_msg
    global output_msg
    if not target == 3: #pinky
        input_msg.append(CHAR_DICT[hand][target][0])
        line_pos_x[0] += 30
        line_pos_x[1] += 30
        CHAR_DICT[hand][target][1] = True
        if len(input_msg) >= 0: # coloring displayed sentence and soundFX when user types
            if test_phrase[len(input_msg)-1] in input_msg[len(input_msg)-1]:
                phrase_chars[len(input_msg)-1][2] = (0, 255, 0)
                playsound("/Users/romanbeier/Documents/Education/Master/TU Wien/04-Master-SoSe23/Masterthesis/Code/tip-top-typing/soundFX/key_press_click.caf")
            else:
                phrase_chars[len(input_msg)-1][2] = (255, 0, 0)
                playsound("/Users/romanbeier/Documents/Education/Master/TU Wien/04-Master-SoSe23/Masterthesis/Code/tip-top-typing/soundFX/keyboard_press_normal.caf")

    else:
        match hand:
            case "Right":
                input_msg += " "
                output_msg += " "
                line_pos_x[0] += 30
                line_pos_x[1] += 30
                playsound("soundFX/key_press_click.caf")
                CHAR_DICT[hand][target][1] = True
            case "Left":
                CHAR_DICT[hand][target][1] = True
                try:
                    phrase_chars[len(input_msg)-1][2] = (105, 105, 105) # turn deleted character gray again
                    input_msg = input_msg[:-1]
                    output_msg = output_msg[:-1]
                    line_pos_x[0] -= 30
                    line_pos_x[1] -= 30
                    playsound("soundFX/key_press_delete.caf")
                except KeyError:
                    pass
                

    print(f"Input Message: {input_msg}")
    
    # # autocompletion
    # result = list(trie.complete(input_msg)) # get list of possible words
    # if len(result) == 1:    # if there is only one result, autocomplete
    #     output_msg += result[0] + " "
    #     print(output_msg)
    #     input_msg = []
    # # time.sleep(0.1)

def char_written(hand, target):
    if CHAR_DICT[hand][target][1] == False:
        return False
    else:
        return True

def vector(t1, t2):
    x = t2[0] - t1[0]
    y = t2[1] - t1[1]
    z = t2[2] - t1[2]
    return (x, y, z)

def print_phrase(phrase): # for printing self written phrase on image
    position = 0
    for char in phrase:
        cv2.putText(cv2_img_processed, char, ((400 + position), 940), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2)
        position += 30
    
while True:
    frame += 1
    success, img = videoCap.read() #reading image
    # img = cv2.flip(img, 1) #mirror image
    # img = cv2.flip(img, -1) #flip image in both directions
    
    # UI
    cv2.rectangle(img, (200,880), (1720,980), (255,255,255), -1) # draw rectangle for text
    # cv2.putText(img, test_phrase, (400, 940), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2) #put test phrase on image
    
    # PIL handover for text on image
    cv2_img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) 
    pil_img = Image.fromarray(cv2_img_rgb)  
    draw = ImageDraw.Draw(pil_img)  
    font = ImageFont.truetype("fonts/RobotoMono-Regular.ttf", 50) # use a truetype font 
    finger_font = ImageFont.truetype("fonts/AtkinsonHyperlegible-Regular.ttf", 30) # accessible font for finger annotations
    for char in phrase_chars.values():
        draw.text(((400 + char[0]), 890), char[1], font=font, fill=char[2])
    cv2_img_processed = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR) 
    cv2.line(cv2_img_processed,(line_pos_x[0], 960),(line_pos_x[1], 960),(105,105,105),5)
    
    #fps calculations
    thisFrameTime = time.time()
    fps = 1 / (thisFrameTime - lastFrameTime)
    lastFrameTime = thisFrameTime
    cv2.putText(cv2_img_processed, f'FPS:{int(fps)}',
        (20, 70),
        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    recHands = hands.process(img) #recognize hands from out image
    multi_hand_landmarks_list = recHands.multi_hand_landmarks
    multi_handedness_list = recHands.multi_handedness
    
    if recHands.multi_hand_landmarks: 
        
        for idx in range(len(multi_hand_landmarks_list)):     
            hand_landmarks = multi_hand_landmarks_list[idx]   
            handedness = multi_handedness_list[idx]           
            hand_label = handedness.classification[0].label 
            
            height, width, _ = img.shape
            thumb_pos = (hand_landmarks.landmark[4].x * width, hand_landmarks.landmark[4].y * height)
            
            # Calculate thumb top position
            thumb_tip_3d = (hand_landmarks.landmark[4].x * width, hand_landmarks.landmark[4].y * height, hand_landmarks.landmark[4].z)
            thumb_ip_3d = (hand_landmarks.landmark[3].x * width, hand_landmarks.landmark[3].y * height, hand_landmarks.landmark[3].z)
            thumb_vector = vector(thumb_ip_3d, thumb_tip_3d)
            thumb_vector = (thumb_vector[0] * 0.3, thumb_vector[1] * 0.3, thumb_vector[2] * 0.3) # scale vector
            thumb_top = ((thumb_tip_3d[0] + thumb_vector[0]), (thumb_tip_3d[1] + thumb_vector[1]), (thumb_tip_3d[2] + thumb_vector[2]))
            
            # Reset input message when pinky tips touch
            if hand_label == "Left":
                left_pinky_tip_pos = ((hand_landmarks.landmark[20].x * width), (hand_landmarks.landmark[20].y * height))
            if hand_label == "Right":
                right_pinky_tip_pos = ((hand_landmarks.landmark[20].x * width), (hand_landmarks.landmark[20].y * height))
            
            try: #exception handling for first iteration with uncomputed right pinky tip
                if distance(left_pinky_tip_pos, right_pinky_tip_pos) <= 20 and not input_msg == []:
                    input_msg = []
                    for char in phrase_chars:
                        phrase_chars[char][2] = (0, 0, 0)
                    cv2.putText(cv2_img_processed, "Input message cleared", (800, 1030), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                    line_pos_x = [400, 430]
                    print("Input message cleared")
                    playsound("soundFX/keyboard_press_clear.caf")
                    time.sleep(0.1)
            except NameError:
                continue
            
            
            # Thumb Annotations
            # cv2.circle(img, (int(thumb_pos[0]), int(thumb_pos[1])), 5, (0, 255, 0), -1) # Draw Circles on thumb tips
            cv2.circle(cv2_img_processed, (int(thumb_top[0]), int(thumb_top[1])), 5, (0, 0, 255), -1) # Draw Circles on elongatetd thumb top position
                        
            
            # Calculate landmark positions for thumb and finger tips, except pinky [from:to:increment]  
            for idx, point in enumerate(hand_landmarks.landmark[8:21:4]):      
                h, w, c = img.shape 
                landmark_pos = (point.x * w, point.y * h)

                cv2.putText(cv2_img_processed, CHAR_DICT[hand_label][idx][0], (int(landmark_pos[0]), int(landmark_pos[1])), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
                
                if distance(thumb_top, landmark_pos) <= 70 and not char_written(hand_label, idx):
                    write_char(hand_label, idx)
                    if len(input_msg) == len(test_phrase): # if input message is as long as test phrase, check if correct                 
                        with open("phrases/phrases2.txt", "r") as f:
                            phrases = f.readlines()
                            test_phrase = phrases[np.random.randint(0, len(phrases))].strip()
                        input_msg = []
                        phrase_chars = {}
                        line_pos_x = [400, 430]
                        for idx, symbol in enumerate(test_phrase):
                            phrase_chars[idx] = [idx * 30, symbol, (105, 105, 105)]

                    
                elif distance(thumb_top, landmark_pos) <= 70 and char_written:
                    pass
                                    
                elif distance(thumb_top, landmark_pos) > 120 and char_written(hand_label, idx):
                    CHAR_DICT[hand_label][idx][1] = False


    cv2.imshow("Cam Output", cv2_img_processed)
    cv2.waitKey(1)       
