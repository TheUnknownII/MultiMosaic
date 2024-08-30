# Import libraries

import cb2
import pytesseract

# Load the image
image = cv2.imread("car_image.jpg")

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Use pytesseract to do OCR on the image
plate_text = pytesseract.image_to_string(gray)

# Clean up the result (remote any unnecessary characters)
plate_text = ''.join(e for e in plate_text if e.isalnum())

print("Detected License Plate:", plate_text)