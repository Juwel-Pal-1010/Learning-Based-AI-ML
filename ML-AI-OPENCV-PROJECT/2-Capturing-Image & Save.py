import cv2

video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()
    if not ret:
        break

    cv2.imshow("Camera Feed", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'): # Press 'q' to quit
        break

    elif key == ord('c'):   # Press 'c' to capture image

        cv2.imwrite("captured_image.jpg", frame)
        print("Image captured and saved as 'captured_image.jpg'")

video.release()
cv2.destroyAllWindows()
