import cv2
import pytesseract
import RPi.GPIO as GPIO
import time
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk

# Initialize the camera
cap = cv2.VideoCapture(0)

# Load the license plate cascade classifier
plate_cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')

def detect_license_plate(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    plates = plate_cascade.detectMultiScale(gray, 1.1, 10)

    for (x, y, w, h) in plates:
        roi = gray[y:y+h, x:x+w]
        text = pytesseract.image_to_string(roi, config='--psm 8')  # Customize OCR config as needed

        if "LICENSE123" in text:  # Replace with your desired license plate
            open_garage_door()

        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

    return frame

def open_garage_door():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    GPIO.output(18, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(18, GPIO.LOW)
    GPIO.cleanup()

def update_frame():
    ret, frame = cap.read()
    if ret:
        frame = detect_license_plate(frame)
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        imgtk = ImageTk.PhotoImage(image=img)
        camera_label.imgtk = imgtk
        camera_label.configure(image=imgtk)
    camera_label.after(10, update_frame)

root = tk.Tk()
root.title("Garage Door License Plate Recognition")

camera_label = Label(root)
camera_label.pack()

update_frame()

root.mainloop()

cap.release()
cv2.destroyAllWindows()
