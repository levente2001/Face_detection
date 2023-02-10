import cv2
import face_recognition
import time
import smtplib
from playsound import playsound
from email.mime.text import MIMEText
import pyttsx3
from gtts import gTTS

engine = pyttsx3.init()
engine.save_to_file("Üdvözlöm Levente. Ajtó kinyitása folyamatban! 10 másodperce van!", "speech.wav")
engine.runAndWait()

# Load the cascade classifier for face detection
face_cascade = cv2.CascadeClassifier('face-detection/haarcascade_frontalface_default.xml')

# Get an image of your face
image_of_you = face_recognition.load_image_file("face-detection/IMG_3733_3.jpeg")

# Get the encodings of your face
your_face_encoding = face_recognition.face_encodings(image_of_you)[0]

#engine.startLoop(True)

tts = gTTS(tld="hu",slow= "False",lang="hu", text="Üdvözlöm Levente. Ajtó kinyitása folyamatban! 10 másodperce van!")
ttsclose = gTTS(lang="hu", text="Ajtó Bezárása!")
ttsfail = gTTS(lang="hu", text="Hiba az arc beazonosításakor!")
tts.save("succes.mp3")
ttsclose.save("close.mp3")
ttsfail.save("fail.mp3")

# Start the camera
camera = cv2.VideoCapture(0)
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
                playsound("succes.mp3")
                # Send an email with the text "face recognized"
                sender_email = "kalolevente@gmail.com"
                receiver_email = "kbela0990@gmail.com"
                password = "durpiofbbomamyws"
                
                message = MIMEText("I am your AI assistant.\n\nI am writing to inform you that YOUR face has been recognized by the camera.\n\nPlease note that this is just an automated message and does not require any action from you.")
                message['Subject'] = "Face Recognition"
                message['From'] = sender_email
                message['To'] = receiver_email
                
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
                server.quit()
                time.sleep(10)
                print("Door CLOSED")
                playsound("close.mp3")
            else: 
                playsound("fail.mp3")
                print("Authentication ERROR!")

        
    # Display the frame
    cv2.imshow("Face Detection", frame)

    # Exit the script if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        engine.endLoop()
        break


# Release the camera and close the window
camera.release()
cv2.destroyAllWindows()
