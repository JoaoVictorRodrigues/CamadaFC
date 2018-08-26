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

# Threads
import threading

# Class
class RX(object):
    """ This class implements methods to handle the reception
        data over the p2p fox protocol
    """

    def __init__(self, fisica):
        """ Initializes the TX class
        """
        self.fisica      = fisica
        self.buffer      = bytes(bytearray())
        self.threadStop  = False
        self.threadMutex = True
        self.READLEN     = 1024

    def thread(self):
        """ RX thread, to send data in parallel with the code
        essa é a funcao executada quando o thread é chamado.
        """
        while not self.threadStop:
            if(self.threadMutex == True):
                rxTemp, nRx = self.fisica.read(self.READLEN)
                if (nRx > 0):
                    self.buffer += rxTemp
                time.sleep(0.01)

    def threadStart(self):
        """ Starts RX thread (generate and run)
        """
        self.thread = threading.Thread(target=self.thread, args=())
        self.thread.start()

    def threadKill(self):
        """ Kill RX thread
        """
        self.threadStop = True

    def threadPause(self):
        """ Stops the RX thread to run

        This must be used when manipulating the Rx buffer
        """
        self.threadMutex = False

    def threadResume(self):
        """ Resume the RX thread (after suspended)
        """
        self.threadMutex = True

    def getIsEmpty(self):
        """ Return if the reception buffer is empty
        """
        if(self.getBufferLen() == 0):
            return(True)
        else:
            return(False)

    def getBufferLen(self):
        """ Return the total number of bytes in the reception buffer
        """
        return(len(self.buffer))

    def getAllBuffer(self, len):
        """ Read ALL reception buffer and clears it
        """
        self.threadPause()
        b = self.buffer[:]
        self.clearBuffer()
        self.threadResume()
        return(b)

    def getBuffer(self,nData, nHead,index_EOP):
        """ Remove n data from buffer
        """
        self.threadPause()
        start1 = nHead
        stop1 = index_EOP

        b           = self.buffer[start1:stop1]
        self.buffer = self.buffer[nData:]


        self.threadResume()
        return(b)

    def getNData(self):
        """ Read N bytes of data from the reception buffer

        This function blocks until the number of bytes is received
        """
#        temPraLer = self.getBufferLen()
#        print('leu %s ' + str(temPraLer) )

        #if self.getBufferLen() < size:
        #    print("ERROS!!! TERIA DE LER %s E LEU APENAS %s", (size,temPraLer))
        while(1):
            if len(self.buffer) >= 8:
                len_head = 8
                start = len_head
                string_eop = bytearray("EOP", "ascii")
                eop_ok = string_eop + bytearray("OK","ascii")

                #print ("EOP_OK: " + eop_ok)
                package = self.buffer
                head = package[:start]
                head_str = head.decode("utf-8")

                while head_str[0] == "0": #Remove os zeros do head pra achar o tamanho dos dados
                    head_str = head_str[1:]
                time.sleep(0.05)

                print (len(str(string_eop)))

                if (int(head_str) + 11) == len(self.buffer):
                    print ("Entrou")
                    try:
                        stop = package.index(string_eop)
                        while stop == package.index(eop_ok):
                            stop.replace(eop_ok,string_eop)
                            stop = package.index(string_eop)
                        dados = package[start:stop]

                        print("EOP está em: ", stop)
                        print("HEAD: ", head.decode("utf-8"))
                        EOP = package[stop:]
                        print("EOP: ", EOP.decode("utf-8"))

                        overhead = (1-(len(dados)/len(package))) *100 #Cálculo do overhead
                        break

                    except Exception as e:
                        print(e)

        return(self.getBuffer(len(dados),start,stop), overhead)

    def clearBuffer(self):
        """ Clear the reception buffer
        """
        self.buffer = b""
