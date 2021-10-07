import serial #biblioteca serial
import time #biblioteca de delay

ser =serial.Serial('COM7', baudrate=9600, timeout=1)
time.sleep(3) #espera o tempo de setup da placa

numeroAmostras = 10

dataFile = open('logFile.txt','w')

def pegarValores(): #requisita o dado do sensor

    ser.write(b'g')
    arduinoData = ser.readline().hex().split('\r\n')

    return arduinoData[0]

while (1): #loop com funções

    userInput = input('Deseja fazer a leitura de dados?\r')

    if userInput == 's':
         for i in range(0,numeroAmostras):
                data = pegarValores()
                data_tx = int(str(data),16)
                print(data_tx)
