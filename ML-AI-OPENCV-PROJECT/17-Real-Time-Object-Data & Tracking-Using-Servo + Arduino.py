import cv2
import numpy as np
import serial
import time

arduino = serial.Serial("COM3", 9600, timeout=1, write_timeout=2)
time.sleep(2)

cap = cv2.VideoCapture(0)
last_angle = None

def detect_red(h,s,v):
    return(h < 10 or h > 160) and s > 100 and v > 100

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([179, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    red_mask = cv2.bitsize_cr(mask1, mask2)

    # Find contours
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest = max(contours, key = cv2.contourArea)
        if cv2.contourArea(largest) > 500:
            x,y,w,h = cv2.boundingRect(largest)
            cx = x + w // 2

            angle = int(np.interp(cx,[0,frame.shape[1]], [0, 180]))
            if angle != last_angle:
                try:
                    arduino.write((str(angle) + '\n').encode())
                    last_angle = angle
                    time.sleep(0.05)
                except serial.SerialTimeoutException:
                    print("Serial write timeout")
                except Exception as e:
                    print(f"Serial error: {e}")

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.circle(frame, (cx, y + h // 2), 5, (0, 255, 0), -1)

            cv2.imshow("Red Object Tracking", frame)

            if cv2.waitKey(1) == 27:
                break

cap.release()
cv2.destroyAllWindows()