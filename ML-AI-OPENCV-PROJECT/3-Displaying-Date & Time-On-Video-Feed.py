import cv2
from datetime import datetime
video = cv2.VideoCapture(0)
while True:
    ret, frame = video.read()
    if not ret:
        break

    # Get current date and time
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

    # Put the date and time text on the frame
    cv2.putText(frame, dt_string, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8,(0, 255, 0), 2)

    # Show the frame
    cv2.imshow("Camera Feed", frame)

    # Quit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()