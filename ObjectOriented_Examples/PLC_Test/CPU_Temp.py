# import wmi

# def get_cpu_temp():
#     w = wmi.WMI(namespace="root\OpenHardwareMonitor")
#     sensors = w.Sensor()
#     for sensor in sensors:
#         if sensor.SensorType == u'Temperature' and 'CPU' in sensor.Name:
#             return f"Current temperature: {sensor.Value}°C"
#     return "Cannot read CPU temperature"

# if __name__ == "__main__":
#     print(get_cpu_temp())

import wmi

c = wmi.WMI()

for cpu in c.Win32_Processor():
    print(f"Processor: {cpu.Name}")
    print(f"Number of Cores: {cpu.NumberOfCores}")
    print(f"Max Clock Speed: {cpu.MaxClockSpeed} MHz")

for mem in c.Win32_PhysicalMemory():
    print(f"Capacity: {int(mem.Capacity) / (1024**3)} GB")
    print(f"Speed: {mem.Speed} MHz")