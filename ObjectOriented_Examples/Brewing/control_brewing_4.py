import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time
import threading
import random
import platform
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque

# Dynamic GPIO import
if platform.system() == "Linux":
    try:
        import RPi.GPIO as GPIO
        print("[INFO] Using RPi.GPIO")
    except ImportError:
        print("[WARNING] RPi.GPIO not found. Using mock GPIO.")
        from mock_gpio import GPIO
else:
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
    return random.uniform(99.0, 100.0)

class BrewingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Brewing System Control")

        self.temperatures = {'Tank1': 0.0, 'Tank2': 0.0, 'Tank3': 0.0}
        self.timers = {'Mashing': 60, 'Brewing': 120}
        self.timer_running = {'Mashing': False, 'Brewing': False}
        self.elapsed_time = {'Mashing': 0, 'Brewing': 0}
        self.valve_status = {'Tank1': False, 'Tank2': False, 'Tank3': False}
        self.pump_status = {'Tank1': False, 'Tank2': False, 'Tank3': False}

        self.temp_data = {'Tank1': deque(maxlen=15*60), 'Tank2': deque(maxlen=15*60), 'Tank3': deque(maxlen=15*60)}

        self.load_images()
        self.setup_gui()
        self.update_temperatures()

    def load_images(self):
        self.valve_closed_img = ImageTk.PhotoImage(Image.open("ObjectOriented_Examples/Brewing/valve_closed.png").resize((50, 50)))
        self.valve_open_img = ImageTk.PhotoImage(Image.open("ObjectOriented_Examples/Brewing/valve_open.png").resize((50, 50)))
        self.pump_off_img = ImageTk.PhotoImage(Image.open("ObjectOriented_Examples/Brewing/pump_off.png").resize((50, 50)))
        self.pump_running_img = ImageTk.PhotoImage(Image.open("ObjectOriented_Examples/Brewing/pump_running.png").resize((50, 50)))

    def setup_gui(self):
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

            valve_label = tk.Label(self.root, image=self.valve_closed_img)
            valve_label.grid(row=row, column=4, padx=5, pady=5)
            setattr(self, f"tank{i}_valve_label", valve_label)

            pump_label = tk.Label(self.root, image=self.pump_off_img)
            pump_label.grid(row=row, column=5, padx=5, pady=5)
            setattr(self, f"tank{i}_pump_label", pump_label)

        self.mashing_timer_label = tk.Label(self.root, text=f"Mashing Timer: 60 min")
        self.mashing_timer_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.brewing_timer_label = tk.Label(self.root, text=f"Brewing Timer: 120 min")
        self.brewing_timer_label.grid(row=3, column=2, columnspan=2, padx=5, pady=5)

        self.elapsed_mashing_label = tk.Label(self.root, text="Elapsed Time: 0:00")
        self.elapsed_mashing_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.elapsed_brewing_label = tk.Label(self.root, text="Elapsed Time: 0:00")
        self.elapsed_brewing_label.grid(row=4, column=2, columnspan=2, padx=5, pady=5)

        self.start_mashing_button = tk.Button(self.root, text="Start Mashing", command=self.start_mashing)
        self.start_mashing_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        self.start_brewing_button = tk.Button(self.root, text="Start Brewing", command=self.start_brewing)
        self.start_brewing_button.grid(row=5, column=2, columnspan=2, padx=5, pady=5)

        tk.Label(self.root, text="Mashing Time (min):").grid(row=6, column=0, padx=5, pady=5)
        self.mashing_time_entry = tk.Entry(self.root)
        self.mashing_time_entry.insert(0, str(self.timers['Mashing']))
        self.mashing_time_entry.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Brewing Time (min):").grid(row=6, column=2, padx=5, pady=5)
        self.brewing_time_entry = tk.Entry(self.root)
        self.brewing_time_entry.insert(0, str(self.timers['Brewing']))
        self.brewing_time_entry.grid(row=6, column=3, padx=5, pady=5)

        self.set_times_button = tk.Button(self.root, text="Set Times", command=self.set_times)
        self.set_times_button.grid(row=7, column=0, columnspan=4, padx=5, pady=5)

        self.show_graph_button = tk.Button(self.root, text="Show Temperature Graph", command=self.open_temperature_graph_window)
        self.show_graph_button.grid(row=8, column=0, columnspan=4, padx=5, pady=5)

    def get_pin(self, tank_number, pin_type):
        # Map tank numbers and pin types to GPIO pin numbers
        pin_map = {
            'Tank1': { 'PUMP': TANK1_PUMP_PIN, 'VALVE': TANK1_VALVE_PIN },
            'Tank2': { 'PUMP': TANK2_PUMP_PIN, 'VALVE': TANK2_VALVE_PIN },
            'Tank3': { 'PUMP': TANK3_PUMP_PIN, 'VALVE': TANK3_VALVE_PIN }
        }
        return pin_map[f'Tank{tank_number}'][pin_type]

    def toggle_pump(self, tank_number):
        pin = self.get_pin(tank_number, "PUMP")
        current_state = GPIO.input(pin)
        GPIO.output(pin, not current_state)
        new_state = "ON" if not current_state else "OFF"
        button = getattr(self, f"tank{tank_number}_pump_button")
        button.config(text=f"Pump {new_state}")

        self.pump_status[f'Tank{tank_number}'] = not current_state
        self.update_pump_image(tank_number)

    def toggle_valve(self, tank_number):
        pin = self.get_pin(tank_number, "VALVE")
        current_state = GPIO.input(pin)
        GPIO.output(pin, not current_state)
        new_state = "ON" if not current_state else "OFF"
        self.valve_status[f'Tank{tank_number}'] = not current_state

        button = getattr(self, f"tank{tank_number}_valve_button")
        button.config(text=f"Valve {new_state}")
        self.update_valve_image(tank_number)

    def update_pump_image(self, tank_number):
        pump_label = getattr(self, f"tank{tank_number}_pump_label")
        if self.pump_status[f'Tank{tank_number}']:
            pump_label.config(image=self.pump_running_img)
        else:
            pump_label.config(image=self.pump_off_img)

    def update_valve_image(self, tank_number):
        valve_label = getattr(self, f"tank{tank_number}_valve_label")
        if self.valve_status[f'Tank{tank_number}']:
            valve_label.config(image=self.valve_open_img)
        else:
            valve_label.config(image=self.valve_closed_img)

    def set_times(self):
        try:
            self.timers['Mashing'] = int(self.mashing_time_entry.get())
            self.timers['Brewing'] = int(self.brewing_time_entry.get())
            self.update_timer_labels()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid integer values for timers.")

    def start_mashing(self):
        if not self.timer_running['Mashing']:
            self.elapsed_time['Mashing'] = 0
            self.timer_running['Mashing'] = True
            threading.Thread(target=self.run_timer, args=('Mashing',)).start()

    def start_brewing(self):
        if not self.timer_running['Brewing']:
            self.elapsed_time['Brewing'] = 0
            self.timer_running['Brewing'] = True
            threading.Thread(target=self.run_timer, args=('Brewing',)).start()

    def run_timer(self, timer_type):
        start_time = time.time()
        while self.elapsed_time[timer_type] < self.timers[timer_type] * 60 and self.timer_running[timer_type]:
            time.sleep(1)
            self.elapsed_time[timer_type] = int(time.time() - start_time)
            self.update_elapsed_time_labels(timer_type)
            self.update_temperature_data()  # Record temperature data for graph
        
        self.elapsed_time[timer_type] = self.timers[timer_type] * 60
        self.update_elapsed_time_labels(timer_type)
        self.timer_running[timer_type] = False
        messagebox.showinfo("Timer", f"{timer_type} Complete!")

    def update_elapsed_time_labels(self, timer_type):
        elapsed_minutes, elapsed_seconds = divmod(self.elapsed_time[timer_type], 60)
        elapsed_time_str = f"{elapsed_minutes}:{elapsed_seconds:02d}"
        
        if timer_type == 'Mashing':
            self.elapsed_mashing_label.config(text=f"Elapsed Time: {elapsed_time_str}")
        else:
            self.elapsed_brewing_label.config(text=f"Elapsed Time: {elapsed_time_str}")

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

        self.update_temperature_data()  # Collect temperature data
        self.root.after(1000, self.update_temperatures)  # Update every second

    def update_temperature_data(self):
        current_time = time.time()
        for tank in ['Tank1', 'Tank2', 'Tank3']:
            self.temp_data[tank].append((current_time, self.temperatures[tank]))

    def open_temperature_graph_window(self):
        graph_window = tk.Toplevel(self.root)
        graph_window.title("Temperature Graph")

        # Create and display the graph
        fig, ax = plt.subplots()
        for tank, data in self.temp_data.items():
            times, temps = zip(*data) if data else ([], [])
            times = [time.strftime('%H:%M:%S', time.gmtime(t)) for t in times]
            ax.plot(times, temps, label=tank)

        ax.set_xlabel('Time')
        ax.set_ylabel('Temperature (°C)')
        ax.set_title('Tank Temperatures over Last 15 Minutes')
        ax.legend()

        fig_canvas = FigureCanvasTkAgg(fig, master=graph_window)
        fig_canvas.draw()
        fig_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            GPIO.cleanup()
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BrewingSystem(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
