plate_cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')  # Use an appropriate classifier

def detect_license_plate(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    plates = plate_cascade.detectMultiScale(gray, 1.1, 10)

    for (x, y, w, h) in plates:
        roi = gray[y:y+h, x:x+w]
        text = pytesseract.image_to_string(roi, config='--psm 8')  # Extract text from the region of interest

        if "LICENSE123" in text:  # Replace with the actual license plate you want to detect
            open_garage_door()

        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

    return frame

def open_garage_door():
    # Code to control the relay to open the garage door
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    GPIO.output(18, GPIO.HIGH)  # Activate the relay
    time.sleep(5)  # Keep the door open for 5 seconds
    GPIO.output(18, GPIO.LOW)  # Deactivate the relay
    GPIO.cleanup()
