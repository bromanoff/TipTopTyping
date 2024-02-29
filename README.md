# TipTopTyping
### Thumb-to-Finger Text Input for Mobile Augmented Reality Applications
TipTopTyping is a vision based thumb-to-finger text input system that allows users to input text by performing pinch gestures between the thumb and the four fingers of each hand. With TipTopTyping, the 26 letters of the english alphabet are grouped into six letter-groups and mapped onto index- middle- and ring-finger of each hand. Space and Delete function reside on the pinky fingers. A trie datastructure forms the basis for storing and recognitizing words. A simple user interface displays the character layout, text input and an autocompletion word preview to perform a simple text copy task.

![screenshot of the user interface](/Figures/QWERTY_typing_example.png)

### CHARACTER LAYOUTS
The user can choose between QWERTY and OPTI character layout. Both layouts arrange letters in groups of at least three but no more than five letters. To adress a letter in a group, the user has to pinch the corresponding finger once. A pseudo word prediction figures out the correct word after a certain amount of input letters.

#### QWERTY
The QWERTY layout maps the letters of a typical QWERTY keyboard on the fingertips in order to resemble the use of a smartphone. Users have to rotate their hands outwards in order to face the palm of the hand. 

![illustration of palm facing QWERTY character layout](/Figures/QWERTY_palm-facing_layout.png)

#### OPTI
The design of OPTI layout is based on findings by [Huang et al. ](https://doi.org/10.1145/2858036.2858483), which described comfort ratings for finger segments and [Xu et al.](https://doi.org/10.1145/3313831.3376306), which found that alternating between hands resulted in slower performances. 

![illustration of optimized OPTI layout](/Figures/OPTI_layout.png)

OPTI builds on these findings and pursues two design considerations:
1. Make frequent letters more accessible by placing them on most comfortable finger segments.
2. Reduce alternation between hands to increase the text entry rate.

Both design considerations are met by grouping the ten most frequent letters in the english language into two groups and placing them on one hand (preferably the dominant hand of the user). Thereby also the nine most frequent bigrams (two-letter sequences) reside on the same hand, thus reducing alternation.

![illustration of OPTI design consideration](/Figures/OPTI_design.png)


## User Study: TipTopTyping Performance & Design

TipTopTyping was tested in a lab-controlled text entry evaluation. 