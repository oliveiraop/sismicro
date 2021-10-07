import serial
import serial.tools.list_ports
import time

#teste = int(input("Numero para ser enviado"))



ser = serial.Serial(
    port='COM5',
    baudrate=9600,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
    )

ser.close()
ser.open()
time.sleep(3)
while(1):
    testeHor = int(input("Digite o numero para testar horizontal: "))
    testeVer = int(input("Digite Teste Vertical: "))

    testeHor = testeHor.to_bytes(2, byteorder='little', signed=False)
    testeVer = testeVer.to_bytes(2, byteorder='little', signed=False)
    ser.write(b'h')
    read_val = ser.read(size=1)
    print(read_val)
    ser.write(testeHor)
    read_val = ser.read(size=1)
    teste = int.from_bytes(read_val, byteorder='little', signed=False)
    print(teste)
    read_val = ser.read(size=1)
    teste = (int.from_bytes(read_val, byteorder='little', signed=False))*256 + teste
    print(teste)
    ser.write(b'v')
    read_val = ser.read(size=1)
    print(read_val)
    ser.write(testeVer)
    read_val = ser.read(size=1)
    teste = int.from_bytes(read_val, byteorder='little', signed=False)
    print(teste)
    read_val = ser.read(size=1)
    teste = (int.from_bytes(read_val, byteorder='little', signed=False))*256 + teste
    print(teste)



comlist = serial.tools.list_ports.comports()
connected = []
for element in comlist:
    connected.append(element.device)
print("Connected COM ports: " + str(connected))