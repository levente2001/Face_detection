import cv2
import numpy as np
import pyautogui

# Load the Haar cascade file for hand detection
hand_cascade = cv2.CascadeClassifier("voice-recognition/hand.xml")

# Initialize the video capture
cap = cv2.VideoCapture(0)

while True:
    # Read the frame
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect hands in the frame
    hands = hand_cascade.detectMultiScale(gray, 1.3, 5)

    # Iterate over the detected hands
    for (x,y,w,h) in hands:
        # Draw a rectangle around the hand
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)

        # Check if the hand is in the left or right half of the frame
        if x+w/2 < frame.shape[1]/2:
            # Hand is in the left half, simulate a left arrow key press
            pyautogui.press('left')
        else:
            # Hand is in the right half, simulate a right arrow key press
            pyautogui.press('right')

    # Display the frame
    cv2.imshow("Hand Detection", frame)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close the window
cap.release()
cv2.destroyAllWindows()

