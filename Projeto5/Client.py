
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
#import cv2
from enlace import *
import time
import matplotlib.pyplot as plt
import binascii
import os
import timeit

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
    arquivo=input("Digite o nome do arquivo que deseja enviar: ")

    # a seguir ha um exemplo de dados sendo carregado para transmissao
    # voce pode criar o seu carregando os dados de uma imagem. Tente descobrir
    #como fazer isso

    #Caso algum dia decidirmos mudar o baudrate, lembrar de mudar essa variavel tambem:)
    baldes=115200
    bitrate=baldes*10
    tamanho=os.stat(arquivo).st_size
    tempo=tamanho/bitrate
    print("O tempo esperado de envio do arquivo é: " + str(tempo))

    print ("gerando dados para transmissao :")

    b = open(arquivo, "rb")
    img_file = b.read()
    txBuffer = img_file
    txLen    = len(txBuffer)

    tipo5 = bytearray("5", "ascii")
    tipo6 = bytearray("6", "ascii")
    while(True):
        print(txLen)
        # Transmite dados
        print("tentado transmitir .... {} bytes".format(txLen))

        start=timeit.default_timer()

        Synched = com.Synch_Client()

        timeout = time.time() + 5
        if Synched == True:
            package = com.tx.organize_package(txLen, img_file, 4) #4 é o tipo da mensagem
            com.sendData(package)

            stop=timeit.default_timer()


            # Atualiza dados da transmissão
            txSize = com.tx.getStatus()

            # Encerra comunicação
            print("-------------------------")
            print("Dados enviados")
            print("-------------------------")

            print("Tempo de envio: ", stop - start)

            received, nRx, overhead = com.getData()
            if (received == tipo5):
                com.tx.threadKill()
                break
            elif (received == tipo6):
                continue
        
        else:
            com.tx.threadKill()
            break

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
