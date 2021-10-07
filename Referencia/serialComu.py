import serial  # biblioteca serial
import time  # biblioteca de delay
from ini_read import getINI

iniData = getINI()
numPoints = int(iniData['numPoints'])  # lê a string do .txt e transforma em inteiro, numero de amostras
numRowsCollect = int(iniData['numRowsCollect'])  # lê a string do .txt e transforma em inteiro, numero de linhas

ser = serial.Serial('COM7', baudrate=9600, timeout=1)
time.sleep(3)  # espera o tempo de setup da placa

dataList = [0]* numPoints
dataFile = open('logFileSr04.txt','w')


def getValues(): #requisita o dado do sensor
    ser.write(b'g')
    arduinoData = ser.readline().hex().split('\r\n')

    return arduinoData[0]

def printToFile(data_tx,index): #adiciona a virgula depois de uma amostra

    dataFile.write(str(data_tx))
    if index != (numPoints - 1):
        dataFile.write(',')
    else:
        dataFile.write('\n')

#def getAverage(dataSet,row):

#    dataAvg = sum(dataSet)/ len(dataSet)
#    print('A média para a linha: ' + str(row) + ' é: ' + str(dataAvg)) #print o numero da linha e a sua média


# Function for calculating median 
def findMedian(dataSet, numPoints): 

    # First we sort the array 
    sorted(a)

    # check for even case 
    if numPoints != 0: 
	return float(dataSet[numPoints/2]) 
	
	return float((dataSet[int((numPoints-1)/2)] + dataSet[int(numPoints/2)])/2.0) 

    print('A mediana para a linha: ' + str(row) + ' é: ' + str(dataAvg)) #print o numero da linha e a sua média

    # Driver program 
    #a = [ 1, 3, 4, 2, 7, 5, 8, 6 ] 
    #n = len(a) 
    #print("Mean =", findMean(a, n)) 
    #print("Median =", findMedian(a, n)) 

# This code is contributed by Smitha Dinesh Semwal 

while (1): #loop com funções

    userInput = input('Deseja fazer a leitura de dados?\r')

    if userInput == 's':
        for row in range(0,numRowsCollect): #numero de linhas
            for i in range(0,numPoints):
                data = getValues()
                s = data
                x = int(s,16)
                data_tx = x*4
                printToFile(data_tx,i) #grava a função no arquivo, pegando a amostra e gravando em sua posição
                dataList[i] = data_tx

            findMedian(dataList,row)
            
        dataFile.close()
        
        break
