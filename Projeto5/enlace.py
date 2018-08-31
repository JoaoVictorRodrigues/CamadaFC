#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Camada de Enlace
####################################################

# Importa pacote de tempo
import time

# Construct Struct
#from construct import *

# Interface Física
from interfaceFisica import fisica

# enlace Tx e Rx
from enlaceRx import RX
from enlaceTx import TX

class enlace(object):
    """ This class implements methods to the interface between Enlace and Application
    """

    def __init__(self, name):
        """ Initializes the enlace class
        """
        self.tipo1 = bytearray("1", "ascii")
        self.tipo2 = bytearray("2", "ascii")
        self.tipo3 = bytearray("3", "ascii")
        self.tipo4 = bytearray("4", "ascii")

        self.fisica      = fisica(name)
        self.rx          = RX(self.fisica)
        self.tx          = TX(self.fisica)
        self.connected   = False

    def enable(self):
        """ Enable reception and transmission
        """
        self.fisica.open()
        self.rx.threadStart()
        self.tx.threadStart()

    def disable(self):
        """ Disable reception and transmission
        """
        self.rx.threadKill()
        self.tx.threadKill()
        time.sleep(1)
        self.fisica.close()

    ################################
    # Application  interface       #
    ################################
    def sendData(self, data):
        """ Send data over the enlace interface
        """
        self.tx.sendBuffer(data)

    def getData(self):
        """ Get n data over the enlace interface
        Return the byte array and the size of the buffer
        """
        print('entrou na leitura e tentara ler ')
        data, overhead = self.rx.getNData()
        
        return(data, len(data), overhead)

    def Synch_Client(self):
        timeout = time.time() + 5 
        #Etapa 1
        print("Synching1")
        txLen1 = len(self.tipo1)
        package = self.tx.organize_package(txLen1, self.tipo1, 1)
        self.sendData(package)
        while(True):
            received , nRx, overhead = self.getData()
            if received == self.tipo2:
                txLen3 = len(self.tipo3)
                package = self.tx.organize_package(txLen3, self.tipo3, 3)
                self.sendData(package)
                print("Synching2")
                return True

            elif time.time() > timeout:
                print("Erro")
        return False
    
    def Synch_Server(self):
        timeout = time.time() + 5
        #Etapa 1
        print("Synching1")
        txLen2 = len(self.tipo2)
        while(True):
            print("Entrou no while")
            received, nRx, overhead = self.getData()
            if (received == self.tipo1):
                package = self.tx.organize_package(txLen2, self.tipo2, 2)
                self.sendData(package)
                print("Synching2")
                while(True):
                    received, nRx, overhead = self.getData()
                    if(received == self.tipo3):
                        print("Synching Done")
                        return True
                    elif time.time() > timeout:
                        print("Erro")
                        break
        return False