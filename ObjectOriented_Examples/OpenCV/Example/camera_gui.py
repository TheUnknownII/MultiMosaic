import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk

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

update_frame()  # Start the camera feed loop

root.mainloop()
