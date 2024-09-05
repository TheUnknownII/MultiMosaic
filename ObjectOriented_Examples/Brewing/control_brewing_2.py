# brewing_system.py

import tkinter as tk
from tkinter import messagebox
import time
import threading
import random  # Replace this with actual sensor readings
import platform

# Dynamic GPIO import
if platform.system() == "Linux":
    try:
        import RPi.GPIO as GPIO
        print("[INFO] Using RPi.GPIO")
    except ImportError:
        print("[WARNING] RPi.GPIO not found. Using mock GPIO.")
        from mock_gpio import GPIO
else:
    # For macOS, Windows, etc., use mock GPIO
    print("[INFO] Non-Linux system detected. Using mock GPIO.")
    from mock_gpio import GPIO

# Setup GPIO pins (Replace these with your actual GPIO pin numbers)
TANK1_PUMP_PIN = 17
TANK1_VALVE_PIN = 27
TANK2_PUMP_PIN = 22
TANK2_VALVE_PIN = 10
TANK3_PUMP_PIN = 9
TANK3_VALVE_PIN = 11

GPIO.setmode(GPIO.BCM)
GPIO.setup(TANK1_PUMP_PIN, GPIO.OUT)
GPIO.setup(TANK1_VALVE_PIN, GPIO.OUT)
GPIO.setup(TANK2_PUMP_PIN, GPIO.OUT)
GPIO.setup(TANK2_VALVE_PIN, GPIO.OUT)
GPIO.setup(TANK3_PUMP_PIN, GPIO.OUT)
GPIO.setup(TANK3_VALVE_PIN, GPIO.OUT)

# Placeholder for actual temperature reading logic
def read_temperature(sensor):
    # Replace this mock with actual sensor reading logic
    return random.uniform(20.0, 100.0)

class BrewingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Brewing System Control")

        self.temperatures = {'Tank1': 0.0, 'Tank2': 0.0, 'Tank3': 0.0}
        self.timers = {'Mashing': 60, 'Brewing': 120}  # in minutes
        self.timer_running = {'Mashing': False, 'Brewing': False}
        self.valve_status = {'Tank1': False, 'Tank2': False, 'Tank3': False}

        self.setup_gui()
        self.update_temperatures()

    def setup_gui(self):
        # Tank Controls
        for i in range(1, 4):
            row = i - 1
            tank_label = tk.Label(self.root, text=f"Tank {i}")
            tank_label.grid(row=row, column=0, padx=5, pady=5)

            temp_label = tk.Label(self.root, text="Temperature: 0.0 °C")
            temp_label.grid(row=row, column=1, padx=5, pady=5)
            setattr(self, f"tank{i}_temp_label", temp_label)

            pump_button = tk.Button(self.root, text="Pump OFF", command=lambda i=i: self.toggle_pump(i))
            pump_button.grid(row=row, column=2, padx=5, pady=5)
            setattr(self, f"tank{i}_pump_button", pump_button)

            valve_button = tk.Button(self.root, text="Valve OFF", command=lambda i=i: self.toggle_valve(i))
            valve_button.grid(row=row, column=3, padx=5, pady=5)
            setattr(self, f"tank{i}_valve_button", valve_button)

            # Add valve indicator (canvas with circle for open/closed)
            valve_canvas = tk.Canvas(self.root, width=50, height=50)
            valve_canvas.grid(row=row, column=4, padx=5, pady=5)
            valve_indicator = valve_canvas.create_oval(10, 10, 40, 40, fill="red")
            setattr(self, f"tank{i}_valve_indicator", valve_indicator)
            setattr(self, f"tank{i}_valve_canvas", valve_canvas)

        # Timer Controls
        self.mashing_timer_label = tk.Label(self.root, text=f"Mashing Timer: {self.timers['Mashing']} min")
        self.mashing_timer_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.brewing_timer_label = tk.Label(self.root, text=f"Brewing Timer: {self.timers['Brewing']} min")
        self.brewing_timer_label.grid(row=3, column=2, columnspan=2, padx=5, pady=5)

        self.start_mashing_button = tk.Button(self.root, text="Start Mashing", command=self.start_mashing)
        self.start_mashing_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.start_brewing_button = tk.Button(self.root, text="Start Brewing", command=self.start_brewing)
        self.start_brewing_button.grid(row=4, column=2, columnspan=2, padx=5, pady=5)

    def toggle_pump(self, tank_number):
        pin = self.get_pin(tank_number, "PUMP")
        current_state = GPIO.input(pin)
        GPIO.output(pin, not current_state)
        new_state = "ON" if not current_state else "OFF"
        button = getattr(self, f"tank{tank_number}_pump_button")
        button.config(text=f"Pump {new_state}")
        print(f"Tank {tank_number} Pump turned {new_state}")

    def toggle_valve(self, tank_number):
        pin = self.get_pin(tank_number, "VALVE")
        current_state = GPIO.input(pin)
        GPIO.output(pin, not current_state)
        new_state = "ON" if not current_state else "OFF"
        self.valve_status[f'Tank{tank_number}'] = not current_state

        # Update button text
        button = getattr(self, f"tank{tank_number}_valve_button")
        button.config(text=f"Valve {new_state}")

        # Update the valve indicator color
        self.update_valve_indicator(tank_number, not current_state)

        print(f"Tank {tank_number} Valve turned {new_state}")

    def get_pin(self, tank_number, component):
        if tank_number == 1:
            return TANK1_PUMP_PIN if component == "PUMP" else TANK1_VALVE_PIN
        elif tank_number == 2:
            return TANK2_PUMP_PIN if component == "PUMP" else TANK2_VALVE_PIN
        elif tank_number == 3:
            return TANK3_PUMP_PIN if component == "PUMP" else TANK3_VALVE_PIN

    def update_valve_indicator(self, tank_number, is_open):
        # Update the color of the valve indicator (green for open, red for closed)
        valve_canvas = getattr(self, f"tank{tank_number}_valve_canvas")
        valve_indicator = getattr(self, f"tank{tank_number}_valve_indicator")
        new_color = "green" if is_open else "red"
        valve_canvas.itemconfig(valve_indicator, fill=new_color)

    def start_mashing(self):
        if not self.timer_running['Mashing']:
            self.timer_running['Mashing'] = True
            threading.Thread(target=self.run_timer, args=('Mashing',)).start()

    def start_brewing(self):
        if not self.timer_running['Brewing']:
            self.timer_running['Brewing'] = True
            threading.Thread(target=self.run_timer, args=('Brewing',)).start()

    def run_timer(self, timer_type):
        while self.timers[timer_type] > 0:
            time.sleep(60)  # Wait for 1 minute
            self.timers[timer_type] -= 1
            self.update_timer_labels()
        
        self.timer_running[timer_type] = False
        messagebox.showinfo("Timer", f"{timer_type} Complete!")

    def update_timer_labels(self):
        self.mashing_timer_label.config(text=f"Mashing Timer: {self.timers['Mashing']} min")
        self.brewing_timer_label.config(text=f"Brewing Timer: {self.timers['Brewing']} min")

    def update_temperatures(self):
        self.temperatures['Tank1'] = read_temperature("Sensor1")
        self.temperatures['Tank2'] = read_temperature("Sensor2")
        self.temperatures['Tank3'] = read_temperature("Sensor3")

        self.tank1_temp_label.config(text=f"Temperature: {self.temperatures['Tank1']:.2f} °C")
        self.tank2_temp_label.config(text=f"Temperature: {self.temperatures['Tank2']:.2f} °C")
        self.tank3_temp_label.config(text=f"Temperature: {self.temperatures['Tank3']:.2f} °C")

        self.root.after(1000, self.update_temperatures)  # Update every second

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            GPIO.cleanup()
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BrewingSystem(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
