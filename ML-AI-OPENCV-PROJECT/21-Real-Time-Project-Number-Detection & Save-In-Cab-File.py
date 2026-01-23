import cv2
import pytesseract
import csv

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\juwel\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml')

image = cv2.imread('Juwel-Car-Plate.jpg')
grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

plates = plate_cascade.detectMultiScale(grey, scaleFactor=1.1, minNeighbors=4)

with open('detected_plates.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Plate Number'])

    for (x, y, w, h) in plates:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        plate_roi = image[y:y + h, x:x + w]

        plate_grey = cv2.cvtColor(plate_roi, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(plate_grey, config='--psm 6')
        print("Detected Plate:", text.strip)
        writer.writerow([text.strip()])

cv2.imshow("Detected Plate", plate_roi)
cv2.imshow("Number Plate Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()


