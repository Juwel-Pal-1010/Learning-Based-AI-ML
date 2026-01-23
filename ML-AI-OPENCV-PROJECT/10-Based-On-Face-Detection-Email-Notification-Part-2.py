import cv2
import smtplib as s
import time

video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

recognizer = cv2.face.LBPHFaceRecognizer.create()
recognizer.read("Trainer.yml")

name_list = ["", "Juwel Pal", "Sanjiban Sihna"]

# Email Configuration

EMAIL_ADDRESS = 'juwelpal1010@gmail.com'
EMAIL_PASSWORD = 'hnot zqrx pyux ynwx'
TO_EMAIL = 'juwelpal1010@gmail.com'

# Limit email sending to once every 30 seconds

last_email_time = 0
EMAIL_INTERVAL = 30 # Seconds

# -------------------------------------------------------------------------------------------------------------

def send_email():
    global last_email_time
    current_time = time.time()
    if current_time - last_email_time >= EMAIL_INTERVAL:
        try:
            m = s.SMTP('smtp.gmail.com', 587)

            m.ehlo()
            m.starttls()
            m.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            m.sendmail(EMAIL_ADDRESS, TO_EMAIL, "Subject: Alert\n\nUnknown face detected !")
            m.close()
            last_email_time = current_time
            print("Email sent: Unknown face detected !")
        except Exception as e:
            print("Email error: ", e)


while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        serial, conf = recognizer.predict(gray[y:y + h, x:x + w])

        if conf < 50:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
            cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)
            cv2.putText(frame, name_list[serial], (x,y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        else:

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
            cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)
            cv2.putText(frame, "Unknown", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            send_email()
    cv2.imshow("Frame", frame)

    k = cv2.waitKey(2)

    if k == ord("q"):
        break

video.release()
cv2.destroyAllWindows()