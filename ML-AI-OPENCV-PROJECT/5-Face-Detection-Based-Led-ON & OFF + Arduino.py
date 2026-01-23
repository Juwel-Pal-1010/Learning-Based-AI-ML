import cv2
import serial
import time

# Connect to arduino (adjust COM port as per your system)
arduino = serial.Serial('COM8', 9600) # Change COM8 to your actual port
time.sleep(2) # Wait for arduino to initialize

# Start the webcam
video = cv2.VideoCapture(0)

# Load the Haar Cascade for face detection
facedetect = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = facedetect.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    if len(faces) > 0:
        arduino.write(b'1') # Face detected: LED ON
        print("led on")
    else:
        arduino.write(b'0') # No face: LED OFF
        print("led off")

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Face Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()