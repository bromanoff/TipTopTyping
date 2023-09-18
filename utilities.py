from typing import Literal

FINGER_LINKS = {"thumb": {"THUMB_IP": 3,
                          "THUMB_TIP": 4},
                "index": {"INDEX_FINGER_DIP": 7,
                          "INDEX_FINGER_TIP": 8},
                "middle": {"MIDDLE_FINGER_DIP": 11,
                           "MIDDLE_FINGER_TIP": 12},
                "ring": {"RING_FINGER_DIP": 15,
                         "RING_FINGER_TIP": 16},
                "pinky": {"PINKY_DIP": 19,
                          "PINKY_TIP": 20}}

_FINGERS = Literal["thumb", "index", "middle", "ring", "pinky"]

# def finger_top(type_: _FINGERS finger , scalar):
#     finger_tip_3d = (hand_landmarks.landmark[4].x * width, hand_landmarks.landmark[4].y * height, hand_landmarks.landmark[4].z)
#     finger_ip_3d = (hand_landmarks.landmark[3].x * width, hand_landmarks.landmark[3].y * height, hand_landmarks.landmark[3].z)
#     finger_vector = vector(thumb_ip_3d, thumb_tip_3d)
#     scaled_vector = (thumb_vector[0] * 0.3, thumb_vector[1] * 0.3, thumb_vector[2] * 0.3) # scale vector
#     finger_top = ((thumb_tip_3d[0] + thumb_vector[0]), (thumb_tip_3d[1] + thumb_vector[1]), (thumb_tip_3d[2] + thumb_vector[2]))