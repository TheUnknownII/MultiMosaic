# mock_gpio.py

class MockGPIO:
    BCM = "BCM"
    OUT = "OUT"
    
    def __init__(self):
        self.pin_states = {}
    
    def setmode(self, mode):
        print(f"[MOCK GPIO] set mode: {mode}")
    
    def setup(self, pin, mode):
        self.pin_states[pin] = False  # Initialize pin state to LOW
        print(f"[MOCK GPIO] setup pin {pin} as {mode}")
    
    def output(self, pin, state):
        self.pin_states[pin] = state
        state_str = "HIGH" if state else "LOW"
        print(f"[MOCK GPIO] pin {pin} set to {state_str}")
    
    def input(self, pin):
        # Return the current state of the pin; default to LOW if not set
        return self.pin_states.get(pin, False)
    
    def cleanup(self):
        print("[MOCK GPIO] cleanup")
        self.pin_states.clear()

# Export the mock class as GPIO
GPIO = MockGPIO()
