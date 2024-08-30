import cv2
import pytesseract
import RPi.GPIO as GPIO
import time

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

def open_garage_door():
    GPIO.output(18, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(18, GPIO.LOW)

def detect_license_plate():
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    cam.release()

    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        plate_text = pytesseract.image_to_string(gray)
        plate_text = ''.join(e for e in plate_text if e.isalnum())
        return plate_text

AUTHORIZED_PLATE = "ABC1234"

while True:
    plate_text = detect_license_plate()
    print("Detected License Plate:", plate_text)

    if plate_text == AUTHORIZED_PLATE:
        print("Authorized plate detected, opening garage door...")
        open_garage_door()
        break

    time.sleep(5)  # Delay between checks
