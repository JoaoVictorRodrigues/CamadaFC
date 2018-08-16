
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
serialName = "COM3"                  # Windows(variacao de)



print("porta COM aberta com sucesso")

def tam_padrao(txLen): #tam_padrao é uma string
    while len(txLen)<6:
        txLen = '0' + txLen
    return txLen

def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName)

    # Ativa comunicacao
    com.enable()

    #verificar que a comunicação foi aberta
    print("comunicação aberta")


    # a seguir ha um exemplo de dados sendo carregado para transmissao
    # voce pode criar o seu carregando os dados de uma imagem. Tente descobrir
    #como fazer isso
    print ("gerando dados para transmissao :")
  
    b = open("img.png", "rb")
    img_file = b.read()
    txBuffer = img_file
    txLen    = len(txBuffer)
    print(txLen)
    txLen = tam_padrao(str(txLen))
    # Transmite dado
    print("tentado transmitir .... {} bytes".format(txLen))
    com.sendData(txLen)
    time.sleep(2)
    com.sendData(txBuffer)

        
    # Atualiza dados da transmissão
    txSize = com.tx.getStatus()

    # Encerra comunicação
    print("-------------------------")
    print("Dados enviados")
    print("-------------------------")
    com.tx.threadKill()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
