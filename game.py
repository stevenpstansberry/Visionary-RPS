import random
import cv2
import HandTrackingModule as htm
import time


def checkWinner(playerChoice, ComputerChoice):
    """
    Determines the winner of the Rock-Paper-Scissors game based on the player's move
    and the computer's move.

    Args:
    - player (str): The player's move ('rock', 'paper', or 'scissors').
    - comp (str): The computer's move ('rock', 'paper', or 'scissors').

    Returns:
    - int: 0 if the player wins, 1 if the computer wins, None if it's a tie.
    """
    if playerChoice == ComputerChoice:
        return None  # Tie
    elif (playerChoice == 'rock' and ComputerChoice == 'scissors') or \
         (playerChoice == 'paper' and ComputerChoice == 'rock') or \
         (playerChoice == 'scissors' and ComputerChoice == 'paper'):
        return 0  # Player wins
    else:
        return 1  # Computer wins


# Game configuration and variables
waitTime = 4  # Time limit for making a move in seconds
moves = ['rock', 'paper', 'scissors']  # Valid moves in the game
scores = [0, 0]  # Scoreboard: [player, computer]
computerChoice, playerChoice = None, None  # Variables to store current moves
wCam, hCam = 1280, 720  # Webcam resolution (width, height)

# Initialize webcam feed
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Initialize hand detection module
detector = htm.handDetector(detectionCon=0.8, maxHands=1) # Detect hands with 80% confidence

# Time variables for frame-per-second (FPS) calculation and game time management
pTime = 0  # Previous time for FPS calculation
prevTime = time.time()  # Time when the previous round ended
newTime = time.time()  # Current time (used for time calculations)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Draw a center line on the screen (for visual effect)
    cv2.line(img, (wCam // 2, 0), (wCam // 2, hCam), (255, 0, 255), 5)

    # Draw a rectangle where the player's hand should be placed
    cv2.rectangle(img, (780, 160), (1180, 560), (0, 165, 255), 2)

     # Display the current scores on the screen
    cv2.putText(img, f'{scores[1]}', (320, 640), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 3)  # Red color
    cv2.putText(img, f'{scores[0]}', (960, 640), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 3)  # Red color

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    # Handling time limit (dark green)
    if waitTime - int(newTime) + int(prevTime) < 0:
        cv2.putText(img, '0', (960, 120), cv2.FONT_HERSHEY_PLAIN, 7, (0, 100, 0), 3)
    else:
        cv2.putText(img, f'{waitTime - int(newTime) + int(prevTime)}', (960, 120), cv2.FONT_HERSHEY_PLAIN, 7, (0, 100, 0), 3)

    # If hand landmarks are detected
    if len(lmList) != 0:

        # Check if the wait time is over for the player to make a move
        if newTime - prevTime >= waitTime:

            x, y = lmList[0][1:] # Get the coordinates of the first landmark (wrist)

            # Check if the player's hand is inside the designated input area
            if 780 < x < 1180 and 160 < y < 560:
                playerChoice = detector.rps()

                computerChoice = moves[random.randint(0, 2)]

                winner = checkWinner(playerChoice, computerChoice)
                if winner is not None:
                    scores[winner] = scores[winner] + 1

                prevTime = time.time()


    #Display computer and player choice
    if newTime - prevTime < 2:
        cv2.putText(img, f'{playerChoice}', (960, 700), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 3)  # Red color
        cv2.putText(img, f'{computerChoice}', (320, 700), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 3)  # Red color
        if computerChoice == 'rock':
            s_img = cv2.imread('images/rock.png')
        elif computerChoice == 'paper':
            s_img = cv2.imread('images/paper.png')
        else:
            s_img = cv2.imread('images/scissors.png')
        x_offset=y_offset=50
        img[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1]] = s_img
        
    # Calculate and display FPS (Frames Per Second)
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
