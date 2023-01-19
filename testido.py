import cv2
import face_recognition
import time
import RPi.GPIO as GPIO

# Load the cascade classifier for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Get an image of your face
image_of_you = face_recognition.load_image_file("IMG_3733_3.jpeg")

# Get the encodings of your face
your_face_encoding = face_recognition.face_encodings(image_of_you)[0]

# Start the camera
camera = cv2.VideoCapture(0)

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)

while True:
    # Read a frame from the camera
    ret, frame = camera.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        detected_face = frame[y:y+h, x:x+w]
        detected_face_encoding = face_recognition.face_encodings(detected_face)

        # Check if this is your face
        if len(detected_face_encoding)>0:
            match = face_recognition.compare_faces([your_face_encoding], detected_face_encoding[0])
            if match[0]:
                print("Door OPENED")
                GPIO.output(18, True)
                GPIO.output(17, False)
                time.sleep(10)
                print("Door CLOSED")
                GPIO.output(18, False)
                GPIO.output(17, True)
                #os.system("afplay /System/Library/Sounds/Basso.aiff")
            else: print("Authentication ERROR!")

        
    # Display the frame
    cv2.imshow("Face Detection", frame)

    # Exit the script if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Release the camera and close the window
camera.release()
cv2.destroyAllWindows()
