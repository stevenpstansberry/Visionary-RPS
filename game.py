import random
import cv2
import HandTrackingModule as htm
import time


def checkWinner(player, comp):
    # Function to determine the winner based on player and computer moves
    if player == comp:
        return None  # Tie
    elif (player == 'rock' and comp == 'scissors') or \
         (player == 'paper' and comp == 'rock') or \
         (player == 'scissors' and comp == 'paper'):
        return 0  # Player wins
    else:
        return 1  # Computer wins


# VARIABLES
waitTime = 4
moves = ['rock', 'paper', 'scissors']
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
        cv2.putText(img, f'{waitTime - int(newTime) + int(prevTime)}', (960, 120), cv2.FONT_HERSHEY_PLAIN, 7, (0, 100, 0), 3)

    # Hand landmarks obtained, next
    if len(lmList) != 0:

        if newTime - prevTime >= waitTime:

            x, y = lmList[0][1:]

            if 780 < x < 1180 and 160 < y < 560:
                player = detector.rps()
                #fingers = detector.fingersUp()
                #totalFingers = fingers.count(1)

                # Game logic
                #if totalFingers == 0:
                #    player = 'rock'
                #elif totalFingers == 2:
                #    player = 'scissor'
                #elif totalFingers == 5:
                #    player = 'paper'

                comp = moves[random.randint(0, 2)]

                winner = checkWinner(player, comp)
                if winner is not None:
                    scores[winner] = scores[winner] + 1

                prevTime = time.time()




    #Display computer and player choice
    if newTime - prevTime < 2:
        cv2.putText(img, f'{player}', (960, 700), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 3)  # Red color
        cv2.putText(img, f'{comp}', (320, 700), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 3)  # Red color
        if comp == 'rock':
            s_img = cv2.imread('images/rock.png')
        elif comp == 'paper':
            s_img = cv2.imread('images/paper.png')
        else:
            s_img = cv2.imread('images/scissors.png')
        x_offset=y_offset=50
        img[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1]] = s_img
        
    # Show fps (blue)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (1050, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    newTime = time.time()

    cv2.imshow('Image', img)
    cv2.waitKey(1)
    
    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
