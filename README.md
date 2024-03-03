# TipTopTyping
### Thumb-to-Finger Text Input for Mobile Augmented Reality Applications
TipTopTyping is a vision based thumb-to-finger text input system that allows users to input text by performing pinch gestures between the thumb and the four fingers of each hand. 

With TipTopTyping, the 26 letters of the English alphabet are grouped into six letter-groups and mapped onto index- middle- and ring-finger of each hand. Space and Delete function reside on the pinky fingers. 

A trie data structure forms the basis for storing and recognizing words. A simple user interface displays the character layout, text input and an autocompletion word preview to perform a simple text copy task.

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
The section below shows overall results for speed (WPM), accuracy (KSPC) and weighted task load (TLXw) of the TipTopTyping performance evaluation 

![table showing results of the evaluation](/Figures/tiptoptyping_performance_4-runs.png)
![table showing results of the evaluation](/Figures/results.png)

#### Speed

The mean entry rate over the whole experiment was 5,92 words per minute (WPM). The average entry speed increased from a mean 5,20 WPM in the first run to a mean 6,74 WPM in the fourth and final run. Two participants were able to type with rates above 10 WPM in the fourth run, just after nine sentences with TipTopTyping.

With a similar amount of practice and more familiarization with the hand tracking, I  was personally able to achieve an input speed of approximately 20 WPM. 

These overall performance scores can be compared to related projects with similar approaches. For example [FingerT9](https://doi.org/10.1145/3132787.3132806) achieved 5,42 WPM on the fifth day of use. [PinchType](https://doi.org/10.1145/3334480.3382888) had a mean speed of 12,54 WPM after a total 40 phrases split over four blocks. With [DigiTouch](https://doi.org/10.1145/3130978) participants typed an average 13 WPM over ten sessions, starting from 7 WPM in the first session and ending with 16 WPM in the last session.

#### Accuracy
The mean accuracy rate over the whole experiment was 1,35 KSPC. In general, participants initially approached the text input technique with caution, attempting to minimize errors even if it meant sacrificing text input speed. Over the course of the study, participants could increase their accuracy from a mean 1,41 keystrokes per character (KSPC) in the first run to 1,33 KSPC in final run.

#### Task Load
Every participant reported and weighted their task load on a scale from 1 to 20 right after each run. The individual weightings were later used to calculate a more precise personal task load score for each participant. Task load scores decreased from 12,10 in the first run to 11,45 in the last run.

![table showing results of the evaluation](/Figures/weighted_diagnostic_TLX%20.png)

The overall Weighted Diagnostic TLX Subscores show, that mental- and performance demand are the most demanding factors. Performance load, in the survey, was describes as the extend to which the participant rated their successful accomplishment of the task set by the experimenter or themselves. In other words, the participants required a high level of mental and perceptual activity and did not consider themselves to be particularly successful at typing. On the other hand, physical and temporal effort as well as frustration was rated relatively low. Frustration was described as the amount of discouragement, irritation, stress and annoyance. The low frustration scores are a little bit surprising regarding the fact that some participant struggled with the interaction method over the whole experiment. It appears that when an interaction is enjoyable or intriguing, it can reduce frustration in the event of failure or when difficulties arise.

### QWERTY vs. OPTI
Participants were typing faster with QWERTY. The mean entry rate for OPTI was 5,67 words per minute (WPM), while users typed an average 6,14 WPM with QWERTY. This is approximately 8,3 % faster. However, typists using the OPTI layout made fewer keystrokes per character compared to using the QWERTY layout, meaning a higher accuracy for OPTI.

![plots comparing performances between layouts](/Figures/results_qwerty-vs-opti.png)

### Standing vs. Walking
Walking has a negative effect on all three performance measures. A comparison between character layouts shows, that walking has a stronger negative effect on OPTI for accuracy and task load. 

![plots comparing performances between mobility scenarios](/Figures/results_standing-vs-walking.png)

Nevertheless, participants were doing less keystrokes per character across all conditions (higher accuracy) with OPTI and were able to increase their accuracy from first to second run with the OPTI layout.

![plots comparing performances between consecutive trials](/Figures/results_consecutive-trials.png)

