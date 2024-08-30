#Import Libraries
import cv2

# Initialize the camera
cam = cv2.VideoCapture(0)
ret, frame = cam.read()

if ret:
    # Save the apcture image
    cv2.imwrite("car_image.jpg", frame)

cam.release()