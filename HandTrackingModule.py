import cv2
import mediapipe as mp


class handDetector():
    """
    A class to detect hands and determine their positions using the Mediapipe library.
    This class can also track the hand's finger positions and make basic predictions
    such as whether the hand forms 'rock', 'paper', or 'scissors'.
    """
    def __init__(self, mode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        """
        Initializes the handDetector object with optional parameters for hand detection.

        Parameters:
        - mode (bool): Whether to run the hand tracking in static mode or not (default is False, meaning it's dynamic).
        - maxHands (int): Maximum number of hands to detect (default is 2).
        - modelComplexity (int): Complexity of the hand landmark model (default is 1).
        - detectionCon (float): Minimum confidence value ([0.0, 1.0]) for hand detection (default is 0.5).
        - trackCon (float): Minimum confidence value ([0.0, 1.0]) for hand tracking (default is 0.5).
        """
        self.mode = mode # Model running mode, default is False
        self.maxHands = maxHands #Maximum number of hands, default is 2
        self.modelComplexity = modelComplexity # Model complexity, default is 1
        self.detectionCon = detectionCon # Detection confidence threshold, default is 0.5
        self.trackCon = trackCon # Tracking confidence threshold, default is 0.5

        # Initialize Mediapipe’s hand detection model and drawing tools
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplexity, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

        # List of fingertip IDs (index in the landmark list that represent fingertips)
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):
        """
        Detect hands in the provided image and draw landmarks if requested.

        Parameters:
        - img (numpy.ndarray): The image in which to detect hands.
        - draw (bool): Whether to draw hand landmarks on the image (default is True).

        Returns:
        - img (numpy.ndarray): The image with drawn hand landmarks (if `draw=True`).
        """
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
        """
        Get the positions of landmarks of the specified hand.

        Parameters:
        - img (numpy.ndarray): The image to process.
        - handNo (int): The index of the hand to get the landmarks for (default is 0).
        - draw (bool): Whether to draw circles on the landmarks (default is True).

        Returns:
        - lmList (list): A list of [id, x, y] for each landmark where:
          - id: The landmark ID.
          - x: The x-coordinate of the landmark.
          - y: The y-coordinate of the landmark.
        """
        self.lmList = []  # List to store landmark positions

        # Check if any hands were detected
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # Convert normalized landmark coordinates to pixel coordinates
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)  # Draw a circle at each landmark

        return self.lmList

    def fingersUp(self):
        """
        Determine which fingers are up by checking their landmarks' positions.

        Returns:
        - fingers (list): A list of 1's (up) and 0's (down) indicating the state of each finger (thumb to pinky).
        """
        fingers = []

        # Check thumb's position (thumb tip < knuckle means thumb is up)
        if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Check the other four fingers (tip < middle joint means finger is up)
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers
    
    def rps(self):
        """
        Determine the player's move in Rock-Paper-Scissors based on which fingers are up.

        Returns:
        - move (str): The player's move ('rock', 'paper', 'scissors', or 'invalid').
        """
        moves = ['rock', 'paper', 'scissors']
        fingers = [] # List to store the state of each finger

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
