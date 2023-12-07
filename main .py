import cv2
import mediapipe as mp



def fingerPosition(image, handNo=0):
    lmList = []
    if results.multi_hand_landmarks:
        myHand = results.multi_hand_landmarks[handNo]
        for id, lm in enumerate(myHand.landmark):
            # print(id,lm)
            h, w, c = image.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id, cx, cy])
    return lmList

def action(detect):
    if '543210' in detect:
        return False
    else:
        return True


flag = 0

tipIds = [4, 8, 12, 16, 20]
dangerSighn = '0'

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

hands = mp.solutions.hands.Hands(max_num_hands=1)
draw = mp.solutions.drawing_utils

while True:
    if flag == 1:
        break



    success, image = vc.read()
    image = cv2.flip(image, 1)
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

            draw.draw_landmarks(image, handLms, mp.solutions.hands.HAND_CONNECTIONS)

    cv2.imshow("Hand", image)
    lmList = fingerPosition(image)
    #print(lmList)

    if len(lmList) != 0:
        fingers = []
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                # state = "Play"
                fingers.append(1)
            if (lmList[tipIds[id]][2] > lmList[tipIds[id] - 2][2]):
                fingers.append(0)

        if abs(lmList[4][1] - lmList[5][1]) > 50:
            fingers.append(1)
        else:
            fingers.append(0)
        totalFingers = fingers.count(1)
        if totalFingers != int(dangerSighn[-1]):
            dangerSighn += str(totalFingers)
        if len(dangerSighn) > 10:
            dangerSighn = dangerSighn[len(dangerSighn)//2:]

        print(totalFingers, fingers, "\t", dangerSighn)
        if action(dangerSighn):
            pass
        else:
            print("HELP")
            flag = 1






