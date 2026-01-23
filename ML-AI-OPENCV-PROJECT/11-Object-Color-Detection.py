import cv2
import numpy as np

# Start Webcam
cap = cv2.VideoCapture(0)

# Function to detect color based on HSV range
def detect_color(h,s,v):
    if s < 50 and v > 200:
        return "White"
    elif v < 50:
        return "Black"
    elif h < 10 or h > 160:
        return "Red"
    elif 10 < h < 25:
        return "Yellow"
    elif 25 < h < 35:
        return "Yellow"
    elif 35 < h < 85:
        return "Green"
    elif 85 < h < 130:
        return "Blue"
    elif 130 < h < 160:
        return "Purple"
    else:
        return "Undefined"

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip frame horizontally
    frame = cv2.flip(frame, 1)

    # Define a small center region for color detection
    height, width, _ = frame.shape
    cx, cy = int(width/2), int(height/2)
    box_size = 10
    roi = frame [cy - box_size:cy + box_size, cx - box_size:cx + box_size]

    # Convert to HSV
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.mean(hsv_roi)[:3]

    # Get detected color
    color_name = detect_color(h,s,v)

    # Draw rectangle & text
    cv2.rectangle(frame, (cx - box_size, cy - box_size), (cx + box_size, cy + box_size), (255, 255, 255), 2)
    cv2.putText(frame, f"Color: {color_name}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    # Show result
    cv2.imshow("Live Color Detection", frame)

    # Exit on ESC key
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()