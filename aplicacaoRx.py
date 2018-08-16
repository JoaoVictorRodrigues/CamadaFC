
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Aplicação
####################################################

print("comecou")
import numpy as np
import cv2
from enlace import *
import time
import matplotlib.pyplot as plt
import binascii

# voce deverá descomentar e configurar a porta com através da qual ira fazer a
# comunicaçao
# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM4"                  # Windows(variacao de)



print("porta COM aberta com sucesso")



def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName)

    # Ativa comunicacao
    com.enable()

    #verificar que a comunicação foi aberta
    print("comunicação aberta")
   

    # Faz a recepção dos dados
    print ("Recebendo dados .... ")
    txLen, nRx2 = int(com.getData(6))
    time.sleep(2)
    rxBuffer, nRx = com.getData(txLen)

    # log
    print ("Lido              {} bytes ".format(nRx))
    
    print (rxBuffer)

    nf = open("imgFile1.png", "wb")
    nf.write(rxBuffer)
    nf.close()

    # Encerra comunicação
    print("-------------------------")
    print("Dados recebidos")
    print("-------------------------")
    com.rx.threadKill()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
