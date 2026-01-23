import cv2
import numpy as np
import csv

# Start webcam
cap = cv2.VideoCapture(0)

# Red color count
red_count = 0

# White color count
white_count = 0

# Track red present status
red_present = False

# Track white present status
white_present = False

# Function to detect red color based on hsv values
def is_red(h, s, v):
    return (h < 10 or h > 160) and s > 100 and v > 100

# Function to detect white color based on hsv values
def is_white(h, s, v):
    return s < 50 and v > 200


while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip frame horizontally
    frame = cv2.flip(frame, 1)

    # Define central region for detection
    height, width, _ = frame.shape
    cx, cy = int(width / 2), int(height / 2)
    box_size = 60
    h_frame = frame[cy - box_size:cy + box_size, cx - box_size:cx + box_size]

    # Convert ROI to HSV
    hsv_roi = cv2.cvtColor(h_frame, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.mean(hsv_roi)[:3]

    color_detected = "None"

    # Check red detection
    if is_red(h,s,v):
        color_detected = "Red"
    if not red_present:
        red_count += 1
        red_present = True
    else:
        red_present = False

    # Check white detection
    if is_white(h,s,v):
        color_detected = "White"
    if not white_present:
        white_count += 1
        white_present = True
    else:
        white_present = False

    # Draw rectangle and text
    cv2.rectangle(frame, (cx - box_size, cy - box_size), (cx + box_size, cy + box_size), (0, 255, 255), 2)
    cv2.putText(frame, f"Color: {color_detected}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    cv2.putText(frame, f"Red Count: {red_count}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    cv2.putText(frame, f"White Count: {white_count}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255,255), 2)

    # Display Result
    cv2.imshow("Red & White Color Detection", frame)

    # Exit on ESC key
    if cv2.waitKey(1) == 27:
        break

# Release Camera
cap.release()
cv2.destroyAllWindows()

# Save red & white count to csv
with open("color_counts.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Color", "Count"])
    writer.writerow(["Red", red_count])
    writer.writerow(["White", white_count])

print("Red & White color counts saved to 'color_counts.csv'")
