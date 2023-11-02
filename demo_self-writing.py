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
import pandas as pd
import os
from openpyxl import load_workbook

part_num = 0

# # QWERTY - Palm facing mental model (note that left/right switched)
# CHAR_DICT = {"Right": {
#     			0: ["qwert", False],
#                 1: ["asdf", False],
#                 2: ["zxc", False],
#                 3: ["SPACE", False]},
#        		"Left": {
#              	0: ["yuiop", False],
#                 1: ["ghjkl", False],
#                 2: ["vbnm", False],
#                 3: ["<-", False]}}

# OPTI - Palm facing mental model (note that left/right switched)
CHAR_DICT = {"Right": {
    			0: ["dcumf", False],
                1: ["pgwtb", False],
                2: ["jqz", False],
                3: ["SPACE", False]},
       		"Left": {
             	0: ["etaoi", False],
                1: ["nsrhl", False],
                2: ["vkx", False],
                3: ["<-", False]}}


# LANGUAGE = ["hut", "haus", "haut", "mut", "maus", "maut", "mann", "hello", "world", "test", "phrase"]
# populate language with every word from phrase
LANGUAGE = []
with open("phrases/phrases2.txt", "r") as file:
    content_without_newlines = ''.join(file.readlines()).replace('\n', ' ')
    words = content_without_newlines.split(" ")
    LANGUAGE.extend(words)
# print(LANGUAGE)

# pull random phrase from phrases2.txt and save it in a variable
with open("phrases/phrases2.txt", "r") as f:
    phrases = f.readlines()
    test_phrase = phrases[np.random.randint(0, len(phrases))].strip()
    
shown_sentences = 1
shown_characters = len(test_phrase)
    
# test_phrase = "hello world test phrase"
# test_phrase = "lost in translation"
# test_phrase = "accompanied by an adult"
test_phrase_words = test_phrase.split(" ")
print("test phrase words: ", test_phrase_words)

phrase_chars = {}
for idx, symbol in enumerate(test_phrase):
    phrase_chars[idx] = [idx * 30, symbol, (50, 50, 50)]
    
# Trie Datastruture to store and query language
trie = Trie()
trie.extend(LANGUAGE)
                  
#opening camera (0 for the default camera, when iPhone continuity camera is active, it will become the default (0))
videoCap = cv2.VideoCapture(0)
lastFrameTime = 0
frame = 0
handSolution = mp.solutions.hands
hands = handSolution.Hands()

completed_words = 0

input_sequence = []
output_msg = ""
word_preview = ""
typed_sentences = 0
typed_words = 0
key_strokes = 0
entered_chars = 0
deleted_chars = 0
action_based_data = {"time": [], "timestamp": [], "action": [], "phrase": [], "word": [], "to type": [], "typed key": []}
action_based_df = pd.DataFrame(columns=["time", "timestamp", "action", "phrase", "word", "to type", "typed key", ])


line_pos_x = [400, 430]

# find whitepsace indices in test phrase
def calculate_phrase_whitespace(phrase):
    from string import whitespace
    test_phrase_whitespace = [i+1 for i, char in enumerate(phrase) if char in whitespace]
    test_phrase_whitespace.insert(0, 0)
    print(test_phrase_whitespace)
    return test_phrase_whitespace

test_phrase_whitespace = calculate_phrase_whitespace(test_phrase)

def distance(pos1, pos2): #pos = (x, y)
    Distance = int(math.sqrt(((pos2[0] - pos1[0]) * (pos2[0] - pos1[0])) + ((pos2[1] - pos1[1]) * (pos2[1] - pos1[1]))))
    return Distance

def word_completed():
    global completed_words
    global typed_words
    try: 
        if output_msg.split(" ")[completed_words] == test_phrase_words[completed_words]:
            completed_words += 1
            typed_words += 1
            print("WORD COMPLETED #########################################################")
            return True
    except IndexError:
        pass
    return False

def slice_at_blankspace(input_sequence):
    if completed_words != 0:
        try:
            blankspace_indices = [i for i, char in enumerate(input_sequence) if char == ' '] # save the index of every blankspace in input sequence
            return input_sequence[blankspace_indices[-1]+1:] 
        except IndexError or TypeError:
            return input_sequence
    else:
        return input_sequence

def write_char(hand, target):
    global input_sequence
    global output_msg
    global word_preview
    global key_strokes
    global entered_chars
    global deleted_chars
    global action_based_df
    global action_based_data
    
    # data collection metrics
    key_strokes += 1
    action_based_data = {"time": [datetime.datetime.now().strftime("%H:%M:%S.%f")],
                         "timestamp": [time.time()],
                         "action": [],
                        "phrase": [test_phrase],
                        "word": [test_phrase_words[completed_words]],
                        "to type": [test_phrase[len(input_sequence)]],
                        "typed key": [CHAR_DICT[hand][target][0]],
                        }
    
    print("Input Sequence on write_char() : ", input_sequence)
    
    if not target == 3: #pinky
        input_sequence.append(CHAR_DICT[hand][target][0])
        cut_input_sequence = slice_at_blankspace(input_sequence)
        print("INPUT SEQUENCE: ", input_sequence)
        print("CUT INPUT SEQUENCE: ", cut_input_sequence)
        print("TEST PHRASE WORDS: ", test_phrase_words)
        trie_list = list(trie.complete(slice_at_blankspace(input_sequence)))
        line_pos_x[0] += 30
        line_pos_x[1] += 30
        CHAR_DICT[hand][target][1] = True
        entered_chars += 1
        action_based_data.update({"action": ["type character"]})
        if len(input_sequence) >= 0: # coloring displayed sentence and soundFX when user types
            try:
                if test_phrase[len(input_sequence)-1] in input_sequence[len(input_sequence)-1]:
                    phrase_chars[len(input_sequence)-1][2] = (0, 255, 0)
                    playsound("/Users/romanbeier/Documents/Education/Master/TU Wien/04-Master-SoSe23/Masterthesis/Code/tip-top-typing/soundFX/key_press_click.caf")
                else:
                    phrase_chars[len(input_sequence)-1][2] = (255, 0, 0)
                    playsound("/Users/romanbeier/Documents/Education/Master/TU Wien/04-Master-SoSe23/Masterthesis/Code/tip-top-typing/soundFX/keyboard_press_normal.caf")
            except KeyError:
                pass
            
################################################### SELF TYPING #########################################################


        # print(f"TRIE LIST: {trie_list}")
        if trie_list == []: # if no candidates are found, add first character of character group to output message
            output_msg += input_sequence[-1][0]
            word_preview = ""
            print("OUTPUT MSG NO TRIE LIST: " + output_msg)
        else:
            if test_phrase_words[completed_words] in trie_list:
                word_preview = test_phrase_words[completed_words]
            # if len(trie_list) == 1:
            #     word_preview = trie_list[0]
            #     print("TRUE WORD PREVIEW: " + word_preview)
            # # TODO: select correct word
            # # FIXME: always display word preview when available for testing without autocompletion
            # elif test_phrase_words[completed_words] == trie_list[-3:]: # for edge cases with abiguous candidates
            #     word_preview = test_phrase_words[completed_words]
            #     print("TRUE WORD PREVIEW: " + word_preview)
            # elif test_phrase_words[completed_words] in trie_list[:len(trie_list)//2]: # workaround for candidate selection
            #     word_preview = test_phrase_words[completed_words]
            #     print("TRUE WORD PREVIEW: " + word_preview)
            else:
                word_preview = trie_list[0]
                print("FALSE WORD PREVIEW: " + word_preview)
                
            for char in input_sequence[-1]: 
                if char == word_preview[len(cut_input_sequence)-1]:
                    output_msg += char
                    output_msg = output_msg.replace(output_msg[-(len(cut_input_sequence)):], word_preview[:len(cut_input_sequence)])
                    print("OUTPUT CASE 0: " + output_msg)
                    break
                else:
                    continue
            else:
                output_msg += input_sequence[-1][0]
                print("OUTPUT CASE 2: " + output_msg)

                
            
            # for char in input_sequence[-1]:                             # for character in last entered group (input_sequence[-1])
            #     if char in test_phrase_words[completed_words][len(cut_input_sequence)-1]:         # if character is equal to character with same index in test phrase
            #         # FIXME: fix word preview when flagged
            #         if word_preview_found:                             # if word completion is only one character long
            #             if output_msg in test_phrase:                   # if output message is equal to test phrase, pass
            #                 pass
            #             else:                                           # if output message is not equal to test phrase, correct output message
            #                 try:
            #                     output_msg += char 
            #                     # print("output_msg BEFORE replacement: " + output_msg)
            #                     # print("word_preview: " + word_preview)
            #                     # print("replace:", output_msg[-(len(cut_input_sequence)):] + " with: " + word_preview[:len(cut_input_sequence)])
            #                     output_msg = output_msg.replace(output_msg[-(len(cut_input_sequence)):], word_preview[:len(cut_input_sequence)]) # replace last entered group with word completion
            #                     # print("output_msg AFTER replacement: " + output_msg)
            #                     break
            #                 except IndexError:
            #                     pass
            #         output_msg += char                              # add character to output message
            #         word_preview_found = False
            #         print("output_msg 1: " + output_msg)
            #     #FIXME: Fix index error: list index out of range
            #     else:
            #         if char in word_preview[len(cut_input_sequence)-1]: # if character is equal to character with same index in word completion
            #             output_msg += char                              # add character to output message
            #             word_preview_found = False
            #             print("output_msg 2: " + output_msg)
            #             break
                    
                        
    
################################################## SELF TYPING ##########################################################

    else: # pinky inputs
        match hand:
            case "Right": # space
                input_sequence += " "
                output_msg += " "
                line_pos_x[0] += 30
                line_pos_x[1] += 30
                entered_chars += 1
                action_based_data.update({"action": ["spacebar"]})
                playsound("soundFX/key_press_click.caf")
                CHAR_DICT[hand][target][1] = True
            case "Left": # delete last character
                CHAR_DICT[hand][target][1] = True
                action_based_data.update({"action": ["delete"]})
                try:
                    phrase_chars[len(input_sequence)-1][2] = (50, 50, 50) # turn deleted character gray again
                    input_sequence = input_sequence[:-1]
                    output_msg = output_msg[:-1]
                    line_pos_x[0] -= 30
                    line_pos_x[1] -= 30
                    entered_chars -= 1
                    deleted_chars += 1
                    playsound("soundFX/key_press_delete.caf")
                except KeyError:
                    pass
    print("----------write action based data----------")
    print(action_based_data)
    action_based_df = pd.concat([action_based_df, pd.DataFrame.from_dict(action_based_data)], ignore_index=True) # add action based data to dataframe

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
    
iterations = 0
while True:
    if frame == 0: #get start time with one time while loop
        start_unix_time = time.time()
        start_time = datetime.datetime.now().strftime("%H:%M:%S.%f")
    frame += 1
    success, img = videoCap.read() #reading image
    # img = cv2.flip(img, 1) #mirror image
    # img = cv2.flip(img, -1) #flip image in both directions
    
    # UI
    cv2.rectangle(img, (200,790), (1720,890), (255,255,255), -1) #draw rectangle for test phrase
    cv2.rectangle(img, (200,900), (1720,1000), (255,255,255), -1) #draw rectangle for text
    # cv2.putText(img, test_phrase, (400, 940), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2) #put test phrase on image
    
    # PIL handover for text on image
    cv2_img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) 
    pil_img = Image.fromarray(cv2_img_rgb)  
    draw = ImageDraw.Draw(pil_img)  
    font = ImageFont.truetype("fonts/RobotoMono-Regular.ttf", 50) # use a truetype font 
    finger_font = ImageFont.truetype("fonts/AtkinsonHyperlegible-Regular.ttf", 30) # accessible font for finger annotations
    # draw.text((400, 790), test_phrase, font=font, fill=(0, 0, 0)) # display test phrase on image
    for char in phrase_chars.values():
        draw.text(((400 + char[0]), 810), char[1], font=font, fill=char[2])
    try:
        draw.text(((400 + (test_phrase_whitespace[completed_words]*30)), 910), word_preview, font=font, fill=(105, 105, 105))
    except IndexError:
        pass
    draw.text(((400), 910), output_msg, font=font, fill=(0, 0, 0))
    cv2_img_processed = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR) 
    cv2.line(cv2_img_processed,(line_pos_x[0], 980),(line_pos_x[1], 980),(105,105,105),5)
    
    #fps calculations
    thisFrameTime = time.time()
    fps = 1 / (thisFrameTime - lastFrameTime)
    lastFrameTime = thisFrameTime
    cv2.putText(cv2_img_processed, f'FPS:{int(fps)}',
        (20, 70),
        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
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
                if distance(left_pinky_tip_pos, right_pinky_tip_pos) <= 20 and not input_sequence == []:
                    completed_words = 0
                    input_sequence = []
                    output_msg = ""
                    word_preview = ""
                    line_pos_x = [400, 450]
                    for char in phrase_chars:
                        phrase_chars[char][2] = (0, 0, 0)
                    cv2.putText(cv2_img_processed, "Input message cleared", (800, 1030), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                    # TODO: check implementation of action based data collection
                    print("----------write action based data----------")
                    print("abd before 'clear' update: ", action_based_data)  
                    action_based_data.update({"action": ["clear"]})
                    print("abd after 'clear' update: ", action_based_data)
                    action_based_df = pd.concat([action_based_df, pd.DataFrame.from_dict(action_based_data)], ignore_index=True) # add action based data to dataframe
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
                # landmark_pos = (int(point.x * w), int(point.y * h))
                landmark_pos = (point.x * w, point.y * h)

                # draw.text((int(landmark_pos[0]), int(landmark_pos[1])), CHAR_DICT[hand_label][idx][0], font=finger_font, fill=(0,0,255))
                # draw.text((100, 100), CHAR_DICT[hand_label][idx][0], font=finger_font, fill=(0,0,255))
                cv2.putText(cv2_img_processed, CHAR_DICT[hand_label][idx][0], (int(landmark_pos[0]), int(landmark_pos[1])), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                
                
                # INFO: detect pinch gesture
                if distance(thumb_top, landmark_pos) <= 70 and not char_written(hand_label, idx):
                    write_char(hand_label, idx)
                    if word_completed():
                        word_preview = ""
                    if len(input_sequence) >= len(test_phrase): # if input message is as long as test phrase, check if correct    
                        iterations += 1
                        typed_sentences += 1
                        if iterations <=2:           
                            with open("phrases/phrases2.txt", "r") as f:
                                phrases = f.readlines()
                                test_phrase = phrases[np.random.randint(0, len(phrases))].strip()
                            shown_sentences += 1
                            shown_characters += len(test_phrase)
                            test_phrase_words = test_phrase.split(" ")
                            completed_words = 0
                            input_sequence = []
                            output_msg = ""
                            phrase_chars = {}
                            word_preview = ""
                            line_pos_x = [400, 430]
                            test_phrase_whitespace = calculate_phrase_whitespace(test_phrase)
                            for idx, symbol in enumerate(test_phrase):
                                phrase_chars[idx] = [idx * 30, symbol, (50, 50, 50)]

                    
                elif distance(thumb_top, landmark_pos) <= 70 and char_written:
                    pass
                                    
                elif distance(thumb_top, landmark_pos) > 120 and char_written(hand_label, idx):
                    CHAR_DICT[hand_label][idx][1] = False


    cv2.imshow("Cam Output", cv2_img_processed)
    k = cv2.waitKey(1) & 0xFF
    # print("key number: ", k)
    if k == 27 or iterations == 3: # close window on ESC or when finished
        ############################## SAVE DATA ########################################
        end_unix_time = time.time()
        end_time = datetime.datetime.now().strftime("%H:%M:%S.%f")
        general_data = {"start unix time": start_unix_time,
                        "start time": start_time,
                        "end time": end_time,
                        "end unix time": end_unix_time,
                        "shown sentences": shown_sentences,
                        "shown characters": shown_characters,
                        "key strokes": key_strokes,
                        "entered chars": entered_chars,
                        "deleted chars": deleted_chars,
                        "typed words": typed_words,
                        "typed sentences": typed_sentences,
                        }
        # print("keys: ", list(general_data.keys()))
        # print("values: ", list(general_data.values()))
        
        print("----------write general data----------")        
        general_data_series = pd.Series(general_data)
        
        # TODO: test if data is saved correctly
        if general_data["typed sentences"] >= 2:
            action_based_df.to_csv("data/action_based_data.csv")
            general_data_series.to_csv("data/general_data.csv")
            with pd.ExcelWriter("data/general_data.xlsx") as writer:
                general_data_series.to_excel(writer, sheet_name=f"Participant {part_num}")
            with pd.ExcelWriter("data/action_based_data.xlsx") as writer:
                action_based_df.to_excel(writer, sheet_name=f"Participant {part_num}")
            print("----------data saved----------")
        
        print(action_based_df)
        print(general_data_series)
        
        cps = key_strokes / round((end_unix_time - start_unix_time),2)
        wpm = cps * 60 / 5
        kspc = key_strokes / entered_chars
        print("----------performance----------")
        print("WPM: ", wpm)
        print("KSPC: ", kspc)
        
        cv2.destroyAllWindows()
        break     
