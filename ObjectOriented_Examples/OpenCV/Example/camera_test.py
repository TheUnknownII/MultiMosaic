import cv2

# Initialize camera with a specified backend
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)  # Use v4l2 backend

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    cv2.imshow('Camera Feed', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()