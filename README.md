# Visionary-RPS

## Project Overview

Visionary-RPS is a Python-based game that allows users to play Rock-Paper-Scissors against the computer using hand gestures. It leverages computer vision via the OpenCV library and MediaPipe for hand tracking, providing a seamless, gesture-based gameplay experience.

## Requirements

This project requires the following libraries:

- `opencv-python` - for capturing video and processing images.
- `mediapipe` - for hand detection and tracking.
- `Pillow` - for handling image operations in the Tkinter GUI.

You can easily install these requirements by running:

```sh
pip install -r requirements.txt
```

## How to run

1. Ensure that you have Python 3.x installed on your machine.
2. Install the required libraries listed above using the provided command.
3. Clone this repository or download the project files.
4. Navigate to the project directory in your terminal or command prompt.
5. Run the application by executing the following command:

```sh
python game.py
```

6. Follow the on-screen instructions to play the game using hand gestures!

## How to Play

1. Launch the program, and you will see a video feed with your camera.
2. Use the following hand gestures to play:

- Rock: Make a fist.
- Paper: Show an open hand.
- Scissors: Extend two fingers (like a "peace" sign).

3. The computer will automatically detect your hand gesture, and the game will determine the winner based on your gesture and the computer's randomly chosen move.

## Features

- Real-time hand gesture recognition using MediaPipe and OpenCV.
- A graphical user interface (GUI) built using Tkinter to control the game.
- A dynamic camera feed that shows the player's hand gestures in real-time.
- Simple game mechanics with automatic detection of hand gestures for rock, paper, and scissors.
- Scoring system that tracks the player's and the computer's wins
