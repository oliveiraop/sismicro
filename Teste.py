comlist = serial.tools.list_ports.comports(include_links=True)
connected = []
for element in comlist:
    print(element.description)
    connected.append(element.device)
print("Connected COM ports: " + str(connected))