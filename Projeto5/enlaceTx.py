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
class TX(object):
    """ This class implements methods to handle the transmission
        data over the p2p fox protocol
    """

    def __init__(self, fisica):
        """ Initializes the TX class
        """
        self.fisica      = fisica
        self.buffer      = bytes(bytearray())
        self.transLen    = 0
        self.empty       = True
        self.threadMutex = False
        self.threadStop  = False

    def thread(self):
        """ TX thread, to send data in parallel with the code
        """
        while not self.threadStop:
            if(self.threadMutex):
                self.transLen    = self.fisica.write(self.buffer)
                #print("O tamanho transmitido. IMpressao dentro do thread {}" .format(self.transLen))
                self.threadMutex = False

    def threadStart(self):
        """ Starts TX thread (generate and run)
        """
        self.thread = threading.Thread(target=self.thread, args=())
        self.thread.start()

    def threadKill(self):
        """ Kill TX thread
        """
        self.threadStop = True

    def threadPause(self):
        """ Stops the TX thread to run

        This must be used when manipulating the tx buffer
        """
        self.threadMutex = False

    def threadResume(self):
        """ Resume the TX thread (after suspended)
        """
        self.threadMutex = True

    def sendBuffer(self, data):
        """ Write a new data to the transmission buffer.
            This function is non blocked.

        This function must be called only after the end
        of transmission, this erase all content of the buffer
        in order to save the new value.
        """
        self.transLen   = 0
        self.buffer = data
        self.threadMutex  = True

    def getBufferLen(self):
        """ Return the total size of bytes in the TX buffer
        """
        return(len(self.buffer))

    def getStatus(self):
        """ Return the last transmission size
        """
        #print("O tamanho transmitido. Impressao fora do thread {}" .format(self.transLen))
        return(self.transLen)
        

    def getIsBussy(self):
        """ Return true if a transmission is ongoing
        """
        return(self.threadMutex)

    def check_EOP(self, pacote, EOP):
        pacote2 = pacote
        index_list = []
        try:
            print("Checando Stuffing", len(pacote))
            if pacote2.index(EOP) < len(pacote):
                while(1):
                    try:
                        index = pacote2.index(EOP)
                        index_list.append(index)
                        pacote2 = pacote[index+len(EOP):]
                        print("EOPs repetidos encontrados: ", index_list)
                        if pacote2.index(EOP) < len(pacote) - 16:
                            continue
                    except Exception as e:
                        return True, index_list
        except Exception as e:
            return False, index_list


    def byte_stuffing(self, index_list, pacote, EOP):
        ok = bytearray("OK", "ascii") 
        for index in index_list:
            pacote[index+len(EOP):index+len(EOP)] = ok
        return pacote

    def tam_padrao(self, txLen, msg_type, num_pacote, total_pacotes, erro_envio): #tam_padrao é uma string
        num_pacote = bytearray(num_pacote)
        total_pacote = bytearray(total_pacotes)
        msg_type = bytearray(msg_type)
        if erro_envio == True:
            erro_envio = bytearray(1)
        else:
            erro_envio = bytearray(0)

        txLen = bytearray(txLen)
        if txLen.decode(int) < 2:
            txLen = bytearray(0) + txLen

        tam_novo = num_pacote+total_pacotes+msg_type+erro_envio+txLen 
        return tam_novo

    def organize_package(self, txLen, pacote, msg_type):
        total_pacotes = txLen//128 + 1

        

        head = self.tam_padrao(txLen, msg_type, num_pacote, total_pacotes, erro_envio)
        EOP = bytearray("EOP", "ascii")
        return head+dados+EOP

