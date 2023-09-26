import cv2
from PIL import ImageFont, ImageDraw, Image  
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

SPRACHE = ["hut", "haus", "haut", "mut", "maus", "maut", "mann", "hello", "world"]  
# test_phrase = "important news always seems to be late"
# pull random phrase from phrases2.txt and save it in a variable
with open("phrases2.txt", "r") as f:
    phrases = f.readlines()
    test_phrase = phrases[np.random.randint(0, len(phrases))].strip()

# test_phrase = "haus maus"
phrase_chars = {}
for idx, symbol in enumerate(test_phrase):
    phrase_chars[idx] = [idx * 30, symbol, (105, 105, 105)]
    
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
output_msg = ""

def distance(pos1, pos2): #pos = (x, y)
    Distance = int(math.sqrt(((pos2[0] - pos1[0]) * (pos2[0] - pos1[0])) + ((pos2[1] - pos1[1]) * (pos2[1] - pos1[1]))))
    return Distance

# def write_char(hand, target):
#     global input_msg
#     global output_msg
#     if not target == 3:
#         input_msg.append(CHAR_DICT[hand][target][0])
#         CHAR_DICT[hand][target][1] = True
#     else:
#         match hand:
#             case "Left":
#                 output_msg += " "
#                 CHAR_DICT[hand][target][1] = True
#             case "Right":
#                 output_msg = output_msg[:-1]
#                 time.sleep(0.2)

def write_char(hand, target):
    global input_msg
    global output_msg
    if not target == 3: #pinky
        input_msg.append(CHAR_DICT[hand][target][0])
        CHAR_DICT[hand][target][1] = True
        for idx, char in enumerate(test_phrase):
            # print(f"idx: {idx}, char: {char}")
            try:
                # FIXME: color letter logic, faulty spcaebar, color reset when backspacing
                if char in input_msg[idx]:
                    phrase_chars[idx][2] = (0, 255, 0)
                else:
                    phrase_chars[idx][2] = (255, 0, 0)
            except IndexError:
                continue
    else:
        match hand:
            case "Right":
                input_msg += " "
                output_msg += " "
                CHAR_DICT[hand][target][1] = True
            case "Left":
                CHAR_DICT[hand][target][1] = True
                try:
                    phrase_chars[len(input_msg)-1][2] = (105, 105, 105) # turn deleted character gray again
                except KeyError:
                    pass
                input_msg = input_msg[:-1]
                output_msg = output_msg[:-1]

    print(f"Input Message: {input_msg}")
    
    # # print child nodes of current char in trie
    # for char in CHAR_DICT[hand_label][idx]:
    #     print(f"Tree children: {trie.children(char)}")
    
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
    # img = cv2.flip(img, 1) #flip image for built in webcam
    
    # UI
    cv2.rectangle(img, (200,880), (1720,980), (255,255,255), -1) #draw rectangle for text
    # cv2.putText(img, test_phrase, (400, 940), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2) #put test phrase on image
    
    # PIL handover for text on image
    cv2_img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) 
    pil_img = Image.fromarray(cv2_img_rgb)  
    draw = ImageDraw.Draw(pil_img)  
    font = ImageFont.truetype("RobotoMono-Regular.ttf", 50) # use a truetype font 
    finger_font = ImageFont.truetype("AtkinsonHyperlegible-Regular.ttf", 30) # accessible font for finger annotations
    for char in phrase_chars.values():
        draw.text(((400 + char[0]), 890), char[1], font=font, fill=char[2]) # put text on image (FIXME: text is not centered)
    cv2_img_processed = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR) 
    
    #fps calculations
    thisFrameTime = time.time()
    fps = 1 / (thisFrameTime - lastFrameTime)
    lastFrameTime = thisFrameTime
    #write on image fps
    cv2.putText(cv2_img_processed, f'FPS:{int(fps)}',
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
            thumb_pos = (hand_landmarks.landmark[4].x * width, hand_landmarks.landmark[4].y * height)
            # print("thumb y-pos: ", hand_landmarks.landmark[4].y * height, "thumb x-pos: ", hand_landmarks.landmark[4].x * width, "thumb-z-pos: ", hand_landmarks.landmark[4].z)
            
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
                if distance(left_pinky_tip_pos, right_pinky_tip_pos) <= 20:
                    input_msg = []
                    for char in phrase_chars:
                        phrase_chars[char][2] = (0, 0, 0)
                    cv2.putText(cv2_img_processed, "Input message cleared", (800, 1030), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                    time.sleep(0.1)
                    print("Input message cleared")
            except NameError:
                continue
            
            
            # Thumb Annotations
            # cv2.circle(img, (int(thumb_pos[0]), int(thumb_pos[1])), 5, (0, 255, 0), -1) # Draw Circles on thumb tips
            # cv2.putText(img, hand_label, (thumb_x, thumb_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2) # print only handedness on thumb
            cv2.circle(cv2_img_processed, (int(thumb_top[0]), int(thumb_top[1])), 5, (0, 0, 255), -1) # Draw Circles on elongatetd thumb top position
                        
            
            # Calculate landmark positions for thumb and finger tips, except pinky [from:to:increment]  
            for idx, point in enumerate(hand_landmarks.landmark[8:21:4]):      
                h, w, c = img.shape 
                # landmark_pos = (int(point.x * w), int(point.y * h))
                landmark_pos = (point.x * w, point.y * h)

                # TODO: change font of finger annotations
                # draw.text((int(landmark_pos[0]), int(landmark_pos[1])), CHAR_DICT[hand_label][idx][0], font=finger_font, fill=(0,0,255))
                cv2.putText(cv2_img_processed, CHAR_DICT[hand_label][idx][0], (int(landmark_pos[0]), int(landmark_pos[1])), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 255), 2)
                
                
                # TODO: Add a variable threshold for distance between thumb and finger tips based on possible next characters, PERMUTATIONS?
                # TODO: OR: Only allow characters that are child nodes of chars in input_msg
                
                if distance(thumb_top, landmark_pos) <= 70 and not char_written(hand_label, idx):
                    write_char(hand_label, idx)
                    if len(input_msg) == len(test_phrase): # if input message is as long as test phrase, check if correct                 
                        with open("phrases2.txt", "r") as f:
                            phrases = f.readlines()
                            test_phrase = phrases[np.random.randint(0, len(phrases))].strip()
                        input_msg = []
                        phrase_chars = {}
                        for idx, symbol in enumerate(test_phrase):
                            phrase_chars[idx] = [idx * 30, symbol, (105, 105, 105)]
                    #     if input_msg == list(test_phrase):
                    #     cv2.putText(cv2_img_processed, "Phrase correct!", (800, 1030), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                    #     time.sleep(0.1)
                    #     print("Phrase correct!")
                    #     test_phrase = refresh_phrase()
                    #     input_msg = []
                    #     output_msg = ""
                    #     for char in phrase_chars:
                    #         phrase_chars[char][2] = (0, 0, 0)
                    # else:
                    #     cv2.putText(cv2_img_processed, "Phrase incorrect!", (800, 1030), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                    #     time.sleep(0.1)
                    #     print("Phrase incorrect!")
                    #     input_msg = []
                    #     output_msg = ""
                    #     for char in phrase_chars:
                    #         phrase_chars[char][2] = (0, 0, 0)
                    
                elif distance(thumb_top, landmark_pos) <= 70 and char_written:
                    pass
                                    
                elif distance(thumb_top, landmark_pos) > 140 and char_written(hand_label, idx):
                    CHAR_DICT[hand_label][idx][1] = False


    cv2.imshow("Cam Output", cv2_img_processed)
    cv2.waitKey(1)       
