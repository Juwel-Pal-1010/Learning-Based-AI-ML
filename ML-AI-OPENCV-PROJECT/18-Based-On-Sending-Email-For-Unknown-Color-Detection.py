import cv2
import numpy as np
import smtplib as s
import time

cap = cv2.VideoCapture(0)

lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([160, 100, 100])
upper_red2 = np.array([179, 255, 255])

EMAIL_ADDRESS = 'juwelpal1010@gmail.com'
EMAIL_PASSWORD = 'hnot zqrx pyux ynwx'
TO_EMAIL = 'juwelpal1010@gmail.com'
last_email_time = 0
EMAIL_INTERVAL = 30

def send_email():
    global last_email_time
    current_time = time.time()
    if current_time - last_email_time >= EMAIL_INTERVAL:
        try:
            m = s.SMTP('smtp.gmail.com', 587)

            m.ehlo()
            m.starttls()
            m.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            m.sendmail(EMAIL_ADDRESS, TO_EMAIL, "Subject: Alert\n\nUnknown color detected !")
            m.close()
            last_email_time = current_time
            print("Email sent: Unknown color detected !")
        except Exception as e:
            print("Email error: ", e)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(mask1,mask2)

    total_mask = cv2.inRange(hsv,(0,100,100), (179,255,255))

    unknown_mask = cv2.bitwise_and(total_mask, cv2.bitwise_not(red_mask))

    contours,_ = cv2.findContours(unknown_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    height, width = frame.shape[:2]
    cx,cy = width // 2, height // 2

    cv2.circle(frame, (cx,cy), 5, (255,255,255), -1)
    cv2.line(frame, (cx-20, cy), (cx+20, cy), (255, 255, 255), 1)
    cv2.line(frame, (cx, cy-20), (cx, cy+20), (255, 255, 255), 1)

    unknown_detected = False

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            unknown_detected = True
            x,y,w,h = cv2.boundingRect(cnt)

            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,255), 2)
            cv2.putText(frame, "Unknown Color", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX,0.7, (0,255,255), 2)
            if unknown_detected:
                send_email()

                cv2.imshow("Unknown Color Detection", frame)

                if cv2.waitKey(1) == 27:
                    break

cap.release()
cv2.destroyAllWindows()


