
import tkinter as tk
from tkinter import ttk
import threading
import time


class PLC:
    def __init__(self):
        self.tags = {}
        self.running = False
        self.gui_running = False

    def add_tags(self, tag_name, initial_value=0):
        """Add a tag to the PLC with an initial value"""
        self.tags[tag_name] = initial_value

    def read_tags(self, tag_name):
        """Read the value of a tag from the PLC"""
        if tag_name in self.tags:
            return self.tags[tag_name]
        else:
            print(f"Tag '{tag_name}' not found.")

    def run(self):
        """Start running the PLC simulation"""
        self.running = True
        print("PLC simulation started.")
        while self.running:
            # Example PLC logic (simple increment of a tag)
            if 'Counter' in self.tags:
                self.tags['Counter'] += 1
            elif 'Sensor3' in self.tags:
                self.tags['Sensor3'] +=3.1416
            time.sleep(1)
            


    def stop(self):
       """Stop the PLC simulation"""
       self.running = False
       print("PLC simulation stopped.")

    def start_gui(self):
        """Start GUI to monitor PLC tags"""
        self.gui_running = True
        root = tk.Tk()
        root.title("PLC Simulator") 

        # Create a frame for displaying tags and values
        tag_frame = ttk.Frame(root, padding="10")
        tag_frame.pack(fill=tk.BOTH, expand=True)

        #Create labels and entry widgets for each tag
        for idx, (tag_name, tag_value) in enumerate(self.tags.items()):
            label = ttk.Label(tag_frame, text=f"{tag_name}:")
            label.grid(row=idx, column=0, padx=5, pady=5, sticky=tk.E)

            entry_var = tk.StringVar(value=str(tag_value))
            entry = ttk.Entry(tag_frame, textvariable=entry_var, state="readonly", width=10)
            entry.grid(row=idx, column=1, padx=5, pady=5)

        def update_values():
            while self.gui_running:
                for idx, (tag_name, tag_value) in enumerate(self.tags.items()):
                    entry_var.set(str(tag_value))
                time.sleep(1)

        # Start a thread to update values continuously
        update_thread = threading.Thread(target=update_values)
        update_thread.start()

        root.mainloop()
        self.gui_running = False
        update_thread.join()

# Example usage:
if __name__ == "__main__":
    # Create an instance of PLC
    plc = PLC()

    # Add tags to simulate inputs, outputs, and memory areas
    plc.add_tags("Sensor1", 0)
    plc.add_tags("Sensor2", 0)
    plc.add_tags("Sensor3", 0)
    plc.add_tags("Counter", 0)

    # Start the PLC simulation and GUI
    plc_thread = threading.Thread(target=plc.run)
    plc_thread.start()

    plc.start_gui()

    # Clean up
    plc.stop()
    plc_thread.join()