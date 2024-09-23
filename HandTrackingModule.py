import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        # Initialize the parameters of the hand detector
        self.mode = mode # Model running mode, default is False
        self.maxHands = maxHands #Maximum number of hands, default is 2
        self.modelComplexity = modelComplexity # Model complexity, default is 1
        self.detectionCon = detectionCon # Detection confidence threshold, default is 0.5
        self.trackCon = trackCon # Tracking confidence threshold, default is 0.5

        # Initialize Mediapipe’s hand detection model and drawing tools
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplexity, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

        # Fingertip ID
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):
        # Detect hands in image
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        # Draw hand key points and connecting lines
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        # Find the location of the key points of the hand
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        return self.lmList

    def fingersUp(self):
        # Check if the finger is raised
        fingers = []

        # Thumb
        if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 Fingers
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers
    
    def rps(self):
        # Check if the finger is raised
        moves = ['rock', 'paper', 'scissors']
        fingers = []

        # Thumb
        if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 Fingers
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        if fingers.count(1) == 0:
            move = moves[0]
        elif fingers.count(1) == 5:
            move = moves[1]
        elif fingers[1] == 1 and fingers[2] == 1:
            move = moves[2]
        else:
            move = 'invalid'

        return move


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        # img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        if len(lmList) != 0:
            print(lmList[8]) # Output the position of hand feature points

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        # Show FPS on image
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        # show image
        cv2.imshow("Image", img)
        cv2.waitKey(1)

