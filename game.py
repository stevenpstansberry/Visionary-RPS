import random
import cv2
import HandTrackingModule as htm
import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Initialize the main application window
app = tk.Tk()
app.title("Visionary RPS")
app.geometry("1280x720")

# Global variables
camera_running = False  # Flag to check if the camera is running
cap = None  # Video capture object

# Game configuration and variables
waitTime = 4  # Time limit for making a move in seconds
moves = ['rock', 'paper', 'scissors']  # Valid moves in the game
scores = [0, 0]  # Scoreboard: [player, computer]
computerChoice, playerChoice = None, None  # Variables to store current moves
wCam, hCam = 1280, 720  # Webcam resolution (width, height)

# Initialize hand detection module
detector = htm.handDetector(detectionCon=0.8, maxHands=1)  # Detect hands with 80% confidence

# Time variables for fps and time limit
pTime = 0
prevTime = time.time()
newTime = time.time()

# Title screen
def show_title_screen():
    """
    Displays the title screen when the application starts.
    """
    title_frame = tk.Frame(app)
    title_frame.pack(expand=True)

    # Title Label
    title_label = tk.Label(title_frame, text="Visionary RPS", font=("Arial", 40), fg="blue")
    title_label.pack(pady=20)

    # Subtitle Label
    subtitle_label = tk.Label(title_frame, text="Harness the power of computer vision!", font=("Arial", 20))
    subtitle_label.pack(pady=10)

    # Start button to navigate to the main menu
    start_button = ttk.Button(title_frame, text="Start", command=lambda: show_main_menu(title_frame))
    start_button.pack(pady=20)

def show_main_menu(title_frame=None):
    """
    Displays the main menu. This function hides the title screen and shows the main menu.
    """
    if title_frame:
        title_frame.pack_forget()  # Hide the title screen

    # Main menu UI
    buttons_frame = tk.Frame(app)
    buttons_frame.pack(pady=20)

    start_button = ttk.Button(buttons_frame, text="Start Game", command=start_game)
    start_button.grid(row=0, column=0, padx=10)

    stop_button = ttk.Button(buttons_frame, text="Stop Game", command=stop_game)
    stop_button.grid(row=0, column=1, padx=10)

    instructions_button = ttk.Button(buttons_frame, text="Instructions", command=show_instructions)
    instructions_button.grid(row=0, column=2, padx=10)

    exit_button = ttk.Button(buttons_frame, text="Exit", command=app.quit)
    exit_button.grid(row=0, column=3, padx=10)

    # Label to display the video feed
    global video_label
    video_label = tk.Label(app)
    video_label.pack()

def checkWinner(playerChoice, computerChoice):
    """
    Determines the winner of the Rock-Paper-Scissors game based on the player's move
    and the computer's move.

    Args:
    - playerChoice (str): The player's move ('rock', 'paper', or 'scissors').
    - computerChoice (str): The computer's move ('rock', 'paper', or 'scissors').

    Returns:
    - int: 0 if the player wins, 1 if the computer wins, None if it's a tie.
    """
    if playerChoice == computerChoice:
        return None  # Tie
    elif (playerChoice == 'rock' and computerChoice == 'scissors') or \
         (playerChoice == 'paper' and computerChoice == 'rock') or \
         (playerChoice == 'scissors' and computerChoice == 'paper'):
        return 0  # Player wins
    else:
        return 1  # Computer wins

def start_game():
    """
    Initializes the video capture and starts the game loop.
    """
    global camera_running, cap, prevTime, newTime
    camera_running = True
    cap = cv2.VideoCapture(0)  # Start video capture from the webcam
    cap.set(3, wCam)
    cap.set(4, hCam)
    prevTime = time.time()
    newTime = time.time()
    show_frame()  # Begin displaying frames

def show_frame():
    """
    Captures frames from the webcam, processes them, and displays them in the GUI.
    """
    global camera_running, cap, scores, computerChoice, playerChoice, pTime, prevTime, newTime
    if camera_running:
        success, img = cap.read()
        if not success:
            print("Failed to capture image")
            return
        img = cv2.flip(img, 1)  # Flip image horizontally

        # Draw a center line on the screen (purple)
        cv2.line(img, (wCam // 2, 0), (wCam // 2, hCam), (255, 0, 255), 5)

        # Draw a rectangle where the player's hand should be placed (orange)
        cv2.rectangle(img, (780, 160), (1180, 560), (0, 165, 255), 2)

        # Display the current scores on the screen (red)
        cv2.putText(img, f'{scores[1]}', (320, 640), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 3)  # Computer score
        cv2.putText(img, f'{scores[0]}', (960, 640), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 3)  # Player score

        # Detect hands and landmarks in the image
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)

        # Handling time limit (dark green)
        newTime = time.time()
        timeRemaining = waitTime - int(newTime - prevTime)
        if timeRemaining < 0:
            cv2.putText(img, '0', (960, 120), cv2.FONT_HERSHEY_PLAIN, 7, (0, 100, 0), 3)
        else:
            cv2.putText(img, f'{timeRemaining}', (960, 120), cv2.FONT_HERSHEY_PLAIN, 7, (0, 100, 0), 3)

        # If hand landmarks are detected
        if len(lmList) != 0:
            # Check if the wait time is over for the player to make a move
            if newTime - prevTime >= waitTime:
                x, y = lmList[0][1:]  # Get the coordinates of the first landmark (wrist)

                # Check if the player's hand is inside the designated input area
                if 780 < x < 1180 and 160 < y < 560:
                    playerChoice = detector.rps()

                    computerChoice = random.choice(moves)

                    winner = checkWinner(playerChoice, computerChoice)
                    if winner is not None:
                        scores[winner] += 1  # Update score (0 = player, 1 = computer)

                    prevTime = time.time()  # Reset the time for the next round

        # Display computer and player choice
        if newTime - prevTime < 2 and playerChoice and computerChoice:
            cv2.putText(img, f'{playerChoice}', (960, 700), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 3)  # Player's move
            cv2.putText(img, f'{computerChoice}', (320, 700), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 3)  # Computer's move

            # Display computer's move image
            if computerChoice == 'rock':
                s_img = cv2.imread('images/rock.png')
            elif computerChoice == 'paper':
                s_img = cv2.imread('images/paper.png')
            else:
                s_img = cv2.imread('images/scissors.png')
            if s_img is not None:
                x_offset, y_offset = 50, 50
                img[y_offset:y_offset + s_img.shape[0], x_offset:x_offset + s_img.shape[1]] = s_img
            else:
                print("Error: Image not found")

        # Calculate and display FPS (blue)
        cTime = time.time()
        fps = 1 / (cTime - pTime + 1e-5)  # Added small value to prevent division by zero
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (1050, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        # Convert the image to RGB and then to PIL format
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgPIL = Image.fromarray(imgRGB)
        imgTK = ImageTk.PhotoImage(image=imgPIL)

        # Display the image in the label
        video_label.imgtk = imgTK
        video_label.configure(image=imgTK)

        # Repeat after an interval to simulate a video
        video_label.after(10, show_frame)
    else:
        cap.release()

def stop_game():
    """
    Stops the game and releases the camera resource.
    """
    global camera_running
    camera_running = False
    cap.release()
    video_label.configure(image='')  # Clear the video feed

def show_instructions():
    """
    Opens a new window displaying the game instructions.
    """
    instructions_window = tk.Toplevel(app)
    instructions_window.title("Instructions")
    instructions_text = """
    Welcome to Visonary Rock Paper Scissors!

    Use computer vision and hand gestures to play the game. The computer will randomly select a move once the countdown expires.

    Instructions:
    - To play 'Rock', make a fist.
    - To play 'Paper', show an open hand.
    - To play 'Scissors', show two fingers (index and middle).

    Place your hand inside the orange rectangle on the screen.
    You have 4 seconds to make your move each round.

    Press 'Exit' to close the game.
    """
    instructions_label = tk.Label(instructions_window, text=instructions_text, justify="left")
    instructions_label.pack(padx=20, pady=20)

# Start by displaying the title screen
show_title_screen()

# Run the application
app.mainloop()
