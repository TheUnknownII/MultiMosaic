import datetime

class Equipment:
    def __init__(self, name):
        self.name = name
        self.usage_log = []

    def log_usage(self, status):
        timestamp = datetime.datetime.now()
        self.usage_log.append((timestamp, status))

    def print_usage_log(self):
        for timestamp, status in self.usage_log:
            print(f"{timestamp}: {self.name} {'ON' if status else 'OFF'}")

def main():
    equipment_name = "Machine A"
    equipment = Equipment(equipment_name)

    while True:
        user_input = input(f"Enter 'ON' to turn {equipment_name} on, 'OFF' to turn it off, or 'exit' to quit: ").strip().lower()

        if user_input == "exit":
            break
        elif user_input == "on":
            equipment.log_usage(True)
        elif user_input == "off":
            equipment.log_usage(False)
        else:
            print("Invalid input. Please enter 'ON', 'OFF', or 'exit'.")

    print("\nUsage Log:")
    equipment.print_usage_log()

if __name__ == "__main__":
    main()
