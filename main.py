from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox
import serial
import serial.tools.list_ports
import time


class Application:
    def __init__(main, master=None):
        main.angVertical = 0.0
        main.angHorizontal = 0.0


        main.fontePadrao = ("Arial", "12")
        main.interfaceSerial = Frame(master)
        main.interfaceSerial["pady"] = 10
        main.interfaceSerial["width"] = 300
        main.interfaceSerial.pack()

        main.conectFrame = Frame(master)
        main.conectFrame["width"] = 300
        main.conectFrame.pack()

        main.anguloVertical = Frame(master)
        main.anguloVertical["width"] = 300
        main.anguloVertical.pack()

        main.anguloHorizontal = Frame(master)
        main.anguloHorizontal["width"] = 300
        main.anguloHorizontal.pack()
        
        main.botoes = Frame(master)
        main.botoes["width"] = 300
        main.botoes.pack()

        main.listPorts = Combobox(main.conectFrame, state='readonly')
        main.listPorts["font"] = main.fontePadrao
        main.listPorts.pack()

        main.conectButton = Button(main.conectFrame, text="Conectar", command=main.conectarSerial)
        main.conectButton["font"] = main.fontePadrao
        main.conectButton.pack(side=LEFT)

        main.refreshButton = Button(main.conectFrame, text="Refresh List", command=main.refreshPorts)
        main.refreshButton["font"] = main.fontePadrao
        main.refreshButton.pack(side=LEFT)

        main.desconectButton = Button(main.conectFrame, text="Desconectar", command=main.desconectarSerial)
        main.desconectButton["state"] = DISABLED
        main.desconectButton["font"] = main.fontePadrao
        main.desconectButton.pack(side=LEFT)

        main.labelVertical = Label(main.anguloVertical, text="Ângulo Vertical")
        main.labelVertical["font"] = main.fontePadrao
        main.labelVertical.pack()

        main.vertical = Entry(main.anguloVertical)
        main.vertical["state"] = DISABLED
        main.vertical["font"] = main.fontePadrao
        main.vertical.pack()

        main.labelHorizontal = Label(main.anguloHorizontal, text="Ângulo Horizontal")
        main.labelHorizontal["font"] = main.fontePadrao
        main.labelHorizontal.pack()

        main.horizontal = Entry(main.anguloHorizontal)
        main.horizontal["state"] = DISABLED
        main.horizontal["font"] = main.fontePadrao
        main.horizontal.pack()

        main.TestLabel = Label(main.anguloHorizontal)
        main.TestLabel["font"] = main.fontePadrao
        main.TestLabel.pack()

        main.GoButton = Button(main.botoes, text='Go', command=main.BotaoGo)
        main.GoButton["state"] = DISABLED
        main.GoButton["font"] = main.fontePadrao
        main.GoButton.pack(side=TOP)

        main.MoveCima = Button(main.botoes, text='^')
        main.MoveCima["state"] = DISABLED
        main.MoveCima["font"] = main.fontePadrao
        main.MoveCima["command"] = main.aumentaVertical
        main.MoveCima.pack(side=TOP)

        main.MoveEsquerda = Button(main.botoes, text='<')
        main.MoveEsquerda["state"] = DISABLED
        main.MoveEsquerda["font"] = main.fontePadrao
        main.MoveEsquerda["command"] = main.diminuiHorizontal
        main.MoveEsquerda.pack(side=LEFT)

        main.MoveBaixo = Button(main.botoes, text='v')
        main.MoveBaixo["state"] = DISABLED
        main.MoveBaixo["font"] = main.fontePadrao
        main.MoveBaixo["command"] = main.diminuiVertical
        main.MoveBaixo.pack(side=LEFT)

        main.MoveDireita = Button(main.botoes, text='>')
        main.MoveDireita["state"] = DISABLED
        main.MoveDireita["font"] = main.fontePadrao
        main.MoveDireita["command"] = main.aumentaHorizontal
        main.MoveDireita.pack(side=RIGHT)

        master.bind('<Left>', main.diminuiHorizontalKey)
        master.bind('<Up>', main.aumentaVerticalKey)
        master.bind('<Right>', main.aumentaHorizontalKey)
        master.bind('<Down>', main.diminuiVerticalKey)



    def ativadesativa(main):
        if main.vertical["state"] == "normal":
            main.vertical["state"] = "disabled"
        else:
            main.vertical["state"] = "normal"

    def BotaoGo(main):
        try:
            valueVertical = float(main.vertical.get())
            valueHorizontal = float(main.horizontal.get())
            if 54 >= valueVertical >= -45 and 90 >= valueHorizontal >= -90:
                main.angVertical = valueVertical
                main.angHorizontal = valueHorizontal
            else:
                main.TestLabel["text"] = "Ângulo fora do range"
            try:
                main.moverHorizontal()
                main.moverVertical()
            except:
                main.TestLabel["text"] = "Erro ao Mover"
        except:
            main.TestLabel["text"] = "Ângulo Invalido"

    def aumentaVerticalKey(main, event):
        if (main.MoveCima["state"] != DISABLED):
            main.aumentaVertical()

    def aumentaVertical(main):
        if main.angVertical <= 54:
            main.angVertical = main.angVertical + 1
            main.vertical.delete(0, END)
            main.vertical.insert(INSERT, main.angVertical)
            main.moverVertical()

    def diminuiVertical(main):
        if main.angVertical >= -45:
            main.angVertical = main.angVertical - 1
            main.vertical.delete(0, END)
            main.vertical.insert(INSERT, main.angVertical)
            main.moverVertical()

    def diminuiVerticalKey(main, event):
        if main.MoveBaixo["state"] != DISABLED:
            main.diminuiVertical()

    def aumentaHorizontalKey(main, event):
        if main.MoveDireita["state"] != DISABLED:
            main.aumentaHorizontal()


    def aumentaHorizontal(main):
        if main.angHorizontal <= 90:
            main.angHorizontal = main.angHorizontal + 1
            main.horizontal.delete(0, END)
            main.horizontal.insert(INSERT, main.angHorizontal)
            main.moverHorizontal()

    def diminuiHorizontal(main):
        if main.angHorizontal >= -90:
            main.angHorizontal = main.angHorizontal - 1
            main.horizontal.delete(0, END)
            main.horizontal.insert(INSERT, main.angHorizontal)
            main.moverHorizontal()

    def diminuiHorizontalKey(main, event):
        if main.MoveEsquerda["state"] != DISABLED:
            main.diminuiHorizontal()

    def refreshPorts(main):
        comlist = serial.tools.list_ports.comports()
        main.PortsDescript = []
        main.PortsNames = []
        for element in comlist:
            main.PortsDescript.append(element.description)
            main.PortsNames.append(element.device)
        main.listPorts["values"] = main.PortsDescript

    def conectarSerial(main):
        teste = main.listPorts.current()
        if (teste == -1):
            main.TestLabel["text"] = "Selecione a porta Serial"
        else:
            serialPort = main.PortsNames[teste]
            main.serialConect = serial.Serial(
                port=serialPort,
                baudrate=9600,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
            )
            main.serialConect.close()
            main.serialConect.open()
            main.TestLabel["text"] = "Aguarde"
            time.sleep(2)
            main.TestLabel["text"] = ""
            main.ativarBotoes()

    def desconectarSerial(main):
        try:
            main.serialConect.close()
            main.desativarBotoes()
            main.TestLabel["text"] = "Serial Desconectado"
        except:
            main.TestLabel["text"] = "Erro ao desconectar"


    def moverHorizontal(main):
        main.serialConect.write(b'h')
        aux = main.transformaHorizontal(main.angHorizontal)
        main.serialConect.write(aux)


    def moverVertical(main):
        main.serialConect.write(b'v')
        aux = main.transformaVertical(main.angVertical)
        main.serialConect.write(aux)


    def ativarBotoes(main):
        main.MoveDireita["state"] = NORMAL
        main.MoveBaixo["state"] = NORMAL
        main.MoveEsquerda["state"] = NORMAL
        main.MoveCima["state"] = NORMAL
        main.GoButton["state"] = NORMAL
        main.vertical["state"] = NORMAL
        main.vertical.insert(INSERT, main.angVertical)
        main.horizontal["state"] = NORMAL
        main.horizontal.insert(INSERT, main.angHorizontal)
        main.desconectButton["state"] = NORMAL
        main.listPorts["state"] = DISABLED
        main.conectButton["state"] = DISABLED
        main.refreshButton["state"] = DISABLED

    def desativarBotoes(main):
        main.MoveDireita["state"] = DISABLED
        main.MoveBaixo["state"] = DISABLED
        main.MoveEsquerda["state"] = DISABLED
        main.MoveCima["state"] = DISABLED
        main.GoButton["state"] = DISABLED
        main.vertical["state"] = DISABLED
        main.horizontal["state"] = DISABLED
        main.desconectButton["state"] = DISABLED
        main.listPorts["state"] = NORMAL
        main.conectButton["state"] = NORMAL
        main.refreshButton["state"] = NORMAL

    def transformaHorizontal(main, number):
        number = number + 90
        number = int((number * 2.556) + 140)
        number = number.to_bytes(2, byteorder='little', signed=False)
        return number

    def transformaVertical(main, number):
        number = number + 45
        number = int(490 - (number * 2.667))
        number = number.to_bytes(2, byteorder='little', signed=False)
        return number


root = Tk()
Application(root)
root.title("Camera Servo")
root.mainloop()


