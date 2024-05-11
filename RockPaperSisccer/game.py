import random
import cv2
import HandTrackingModule as htm
import time


def checkWinner(player, comp):
    # Function to determine the winner based on player and computer moves
    if player == comp:
        return None  # Tie
    elif (player == 'rock' and comp == 'scissor') or \
         (player == 'paper' and comp == 'rock') or \
         (player == 'scissor' and comp == 'paper'):
        return 0  # Player wins
    else:
        return 1  # Computer wins


# VARIABLES
waitTime = 4
moves = ['rock', 'paper', 'scissor']
scores = [0, 0]  # [player, comp]
comp, player = None, None
wCam, hCam = 1280, 720

# Get feed from carma
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Initialize hand detection module
detector = htm.handDetector(detectionCon=0.8, maxHands=1)

# Time variables for fps and time limit
pTime = 0
prevTime = time.time()
newTime = time.time()

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Drawing centre line (purple)
    cv2.line(img, (wCam // 2, 0), (wCam // 2, hCam), (255, 0, 255), 5)

    # Area for input (orange)
    cv2.rectangle(img, (780, 160), (1180, 560), (0, 165, 255), 2)

    # Scores (red)
    cv2.putText(img, f'{scores[1]}', (320, 640), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 3)  # Red color
    cv2.putText(img, f'{scores[0]}', (960, 640), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 3)  # Red color

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    # Handling time limit (dark green)
    if waitTime - int(newTime) + int(prevTime) < 0:
        cv2.putText(img, '0', (960, 120), cv2.FONT_HERSHEY_PLAIN, 7, (0, 100, 0), 3)
    else:
        cv2.putText(img, f'{waitTime - int(newTime) + int(prevTime)}', (960, 120), cv2.FONT_HERSHEY_PLAIN, 7,
                    (0, 100, 0), 3)

    # Hand landmarks obtained, next
    if len(lmList) != 0:

        if newTime - prevTime >= waitTime:

            x, y = lmList[0][1:]

            if 780 < x < 1180 and 160 < y < 560:
                fingers = detector.fingersUp()
                totalFingers = fingers.count(1)

                # Game logic
                if totalFingers == 0:
                    player = 'rock'
                elif totalFingers == 2:
                    player = 'scissor'
                elif totalFingers == 5:
                    player = 'paper'

                comp = moves[random.randint(0, 2)]

                winner = checkWinner(player, comp)
                if winner is not None:
                    scores[winner] = scores[winner] + 1

                prevTime = time.time()


    # Update the image
    if comp:
        # read the picture file
        original_img = cv2.imread(f'Fingers/{comp}.jpg')
        if original_img is not None:
            # Resize image to 400x400 pixels
            resized_img = cv2.resize(original_img, (400, 400))
            # Place the resized image into the specified area
            img[160:560, 120:520] = resized_img
        else:
            print("Error：can't read the picture. Please try again.")

    # Show fps (blue)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (1050, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    newTime = time.time()

    cv2.imshow('Image', img)
    cv2.waitKey(1)