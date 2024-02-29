# TipTopTyping
### Thumb-to-Finger Text Input for Mobile Augmented Reality Applications
TipTopTyping is a vision based thumb-to-finger text input system that allows users to input text by performing pinch gestures between the thumb and the four fingers of each hand. With TipTopTyping, the 26 letters of the english alphabet are grouped into six letter-groups and mapped onto index- middle- and ring-finger of each hand. Space and Delete function reside on the pinky fingers. A trie datastructure forms the basis for storing and recognitizing words. A simple user interface displays the character layout, text input and an autocompletion word preview to perform a simple text copy task.

![screenshot of the user interface](/Figures/QWERTY_typing_example.png)

### Character Layouts
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

### Study Design

TipTopTyping was evaluated in a lab-controlled user study with 20 participants. Metrics for text entry performance included Words per Minute (WPM) based on [MacKenzie & Soukoreff](https://doi.org/10.1207/S15327051HCI172&3_2) for text entry rate and [Keystrokes per Character (KSPC)](https://link.springer.com/chapter/10.1007/3-540-45756-9_16) as measure of accuracy. The users task load was assessed by using the NASA TLX questionnaire.

The study followed a 2 x 2 within-subjects factorial design, resulting in four different conditions.

The two factors and their respective levels were:

1. Character Layout
    - QWERTY
    - OPTI
2. Mobility Scenario
    - Standing 
    - Walking

The four corresponding conditions were: 

1. QWERTY - Standing
2. QWERTY - Walking
3. OPTI - Standing
4. OPTI - Walking

The order of conditions was counterbalanced across all participants.

Participant had to copy three phrases from the [MacKenzie Phrase Set](https://www.yorku.ca/mack/chi03b.html) over four blocks of text copy task. One block for each condition. One of the phrases is depicted in the first image on this page. 

## Results
### Overall
The section below shows overall results of the thumb-to-finger text input method 

![table showing results of the evaluation](/Figures/results.png)

#### Speed

The mean entry rate over the whole experiment was 5,92 words per minute (WPM). The average entry speed increased from a mean 5,20 WPM in the first run to a mean 6,74 WPM in the fourth and final run. Two participants were able to type with rates above 10 WPM in the fourth run, just after nine sentences with TipTopTyping.

#### Accuracy
The mean accuracy rate over the whole experiment was 1,35 KSPC. In general, participants initially approached the text input technique with caution, attempting to minimize errors even if it meant sacrificing text input speed. Over the course of the study, participants could increase their accuracy from a mean 1,41 keystrokes per character (KSPC) in the first run to 1,33 KSPC in final run.

#### Task Load
Every participant reported and weighted their task load on a scale from 1 to 20 right after each run. The individual weightings were later used to calculate a more precise personal task load score for each participant. Task load scores decreased from 12,10 in the first run to 11,45 in the last run.

### QWERTY vs. OPTI
Participants were typing faster with QWERTY. The mean entry rate for OPTI was 5,67 words per minute (WPM), while users typed an average 6,14 WPM with QWERTY. This is approximately 8,3 % faster. However, typists using the OPTI layout made fewer keystrokes per character compared to using the QWERTY layout, meaning a higher accuracy for OPTI.

![plots showing comparison of layout performances](/Figures/results_qwerty-vs-opti.png)

