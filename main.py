import cv2 as cv
import numpy as np
import tkinter as tk
from tkinter import ttk
import threading

def on_slider_change(slider_var, value):
    # Update the corresponding lower value based on the slider_var
    if slider_var == h_var:
        lower[0] = int(round(float(value)))
    elif slider_var == s_var:
        lower[1] = int(round(float(value)))
    elif slider_var == v_var:
        lower[2] = int(round(float(value)))

    # Update the label text
    label.config(text=f"Selected values: H={lower[0]}, S={lower[1]}, V={lower[2]}")

def opencv_loop():
    cap = cv.VideoCapture(0)
    while True:
        # Take each frame
        _, frame = cap.read()

        # Convert BGR to HSV
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # Update upper range for HSV based on current slider values
        upper = np.array([int(round(h_var.get())) + 10, 255, 255])

        # Create a mask using the lower and upper HSV values
        mask = cv.inRange(hsv, lower, upper)

        # Apply the mask to the original frame
        res = cv.bitwise_and(frame, frame, mask=mask)

        # Display the frames
        cv.imshow('frame', frame)
        cv.imshow('mask', mask)
        cv.imshow('res', res)

        # Check for the 'Esc' key to exit
        k = cv.waitKey(5) & 0xFF
        if k == 27:
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv.destroyAllWindows()

# Create the main window
root = tk.Tk()
root.title("HSV Sliders")

# Create a label to display the selected values
label = tk.Label(root, text="Selected values: H=0, S=0, V=0")
label.pack(pady=10)

# Create sliders for H, S, and V with IntVar
h_var = tk.IntVar()
s_var = tk.IntVar()
v_var = tk.IntVar()

h_slider = ttk.Scale(root, from_=0, to=255, orient="horizontal", variable=h_var,
                     command=lambda value: on_slider_change(h_var, value))
s_slider = ttk.Scale(root, from_=0, to=255, orient="horizontal", variable=s_var,
                     command=lambda value: on_slider_change(s_var, value))
v_slider = ttk.Scale(root, from_=0, to=255, orient="horizontal", variable=v_var,
                     command=lambda value: on_slider_change(v_var, value))

h_slider.pack()
s_slider.pack()
v_slider.pack()

# Initialize the lower HSV values
lower = np.array([0, 0, 0])

# Start the OpenCV loop in a separate thread
opencv_thread = threading.Thread(target=opencv_loop)
opencv_thread.start()

# Run the Tkinter event loop
root.mainloop()
