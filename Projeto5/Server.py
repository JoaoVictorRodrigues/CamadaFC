
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

    while(True):

        Synched = com.Synch_Server()

        if Synched == True:
            # Faz a recepção dos dados
            print ("Recebendo dados .... ")
            
            rxBuffer, nRx, overhead = com.getData()
            if com.rx.head_match == True:
                print("Dados recebidos: ",len(rxBuffer))
                print("Overhead: ", overhead)

                #txLen, nRx2 = com.getData(6)
                #txLen = int(txLen)

                baldes=115200
                bitrate=baldes*10
                tamanho=nRx
                tempo=tamanho/bitrate
                print("O tempo esperado de envio do arquivo é: " + str(tempo))

                #time.sleep(2)
                #rxBuffer, nRx = com.getData(txLen)

                # log
                print ("Lido              {} bytes ".format(nRx))
                nome2=input("Como você gostaria de nomear o arquivo? : ")

                txLen = bytearray("5", "ascii")
                package = com.tx.organize_package(txLen, img_file, 5)
                com.sendData(package)

                nf = open(nome2, "wb")
                nf.write(rxBuffer)
                nf.close()

                # Encerra comunicação
                print("-------------------------")
                print("Dados recebidos")
                print("-------------------------")


                com.disable()
            else:
                txLen = bytearray("6", "ascii")


    else:
        com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
