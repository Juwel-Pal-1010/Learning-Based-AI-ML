import cv2
import numpy as np

# Webcam setup
cap = cv2.VideoCapture(0)

# HSV red color range
lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([160, 100, 100])
upper_red2 = np.array([179, 255, 255])

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip frame for mirror view
    frame = cv2.flip(frame, 1)

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red mask (both ends are of red hue)
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    red_mask = cv2.bitsize_cr(mask1, mask2)

    # Find contours
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw center guide
    height, width = frame.shape[:2]
    cx, cy = width // 2, height // 2

    cv2.circle(frame, (cx, cy), 5, (255, 255, 255), -1)
    cv2.line(frame, (cx - 20, cy), (cx + 20, cy), (255, 255, 255), 1)
    cv2.line(frame, (cy, cy - 20), (cy, cy + 20), (255, 255, 255), 1)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 5000:
            found_red = True
            x, y, w, h = cv2.boundingRect(cnt)
            obj_cx = x + w // 2
            obj_cy = y + h // 2

            # Draw bounding box and label
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.circle(frame, (obj_cx, obj_cy), 5, (0, 255, 255), -1)
            cv2.putText(frame, "Red Detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)


    # Show the result
    cv2.imshow("Red Color Tracker", frame)

    # Exit on ESC
    if cv2.waitKey(1) == 27:
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
