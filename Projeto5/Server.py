
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
serialName = "COM6"                  # Windows(variacao de)

print("porta COM aberta com sucesso")

def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName)

    # Ativa comunicacao
    com.enable()

    #verificar que a comunicação foi aberta
    print("comunicação aberta")

    done = False
    while(done == False):
        tipo5 = bytearray("5", "ascii")
        tipo6 = bytearray("6", "ascii")
        tipo7 = bytearray("7", "ascii")
        tipo8 = bytearray("8", "ascii")
        Synched = com.Synch_Server()

        if Synched == True:
            # Faz a recepção dos dados
            print ("Recebendo dados .... ")

            while(done == False):
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

                    # Encerra comunicação
                    print("-------------------------")
                    print("Dados recebidos")
                    print("-------------------------")

                    timeout = time.time() + 15
                    while(True):
                        print("Esperando confirmação de envio")
                        received, nRx, overhead = com.getData()
                        if (received == tipo7):
                            nome2=input("Como você gostaria de nomear o arquivo? : ")
                            nf = open(nome2, "wb")
                            nf.write(rxBuffer)
                            nf.close()

                            txLen5 = len(tipo5)
                            package = com.tx.organize_package(txLen5, tipo5, 5)
                            com.sendData(package)
                            time.sleep(1)

                            print("Done")
                            done = True
                            com.disable()
                            break

                else:
                    print("Erro tipo 6")
                    txLen6 = len(tipo6)
                    package = com.tx.organize_package(txLen6, tipo6, 6, True)
                    com.sendData(package)


    else:
        com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
