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
import crcmod
import crcmod.predefined

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

    def sendBuffer(self, sub_pacote):
        """ Write a new data to the transmission buffer.
            This function is non blocked.

        This function must be called only after the end
        of transmission, this erase all content of the buffer
        in order to save the new value.
        """
        self.transLen   = 0
        self.buffer = sub_pacote
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
                        if pacote2.index(EOP) < len(pacote) - 12:
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

    def tam_padrao(self, crc, txLen, msg_type, num_pacote, total_pacotes, erro_envio = False): #tam_padrao é uma string
        num_pacote = num_pacote.to_bytes(1, "big")
        total_pacotes = total_pacotes.to_bytes(1, "big")
        msg_type = msg_type.to_bytes(1, "big")
        if erro_envio == True:
            true = 1
            erro_envio = true.to_bytes(1, "big")
        else:
            false = 0
            erro_envio = false.to_bytes(1, "big")

        txLen = txLen.to_bytes(2, "big")

        crc = crc.to_bytes(2, "big")

        tam_novo = num_pacote+total_pacotes+msg_type+erro_envio+txLen+crc
        return tam_novo


    def sub_packages(self, txLen, pacote):
        total_pacotes = txLen//128
        if (txLen%128 != 0):
            total_pacotes+=1

        #Variáveis definidas para dividir o pacote em fragmentos
        n0 = 0
        n = 128
        p=0
        lista_pacotes = []
        while(p <= total_pacotes-1):
            lista_pacotes.append(pacote[n0:n])
            n0+=128
            n+=128
            p+=1
        lista_pacotes.append(pacote[n:])
        for i in range(len(lista_pacotes)):
            if lista_pacotes[i] == b"":
                del lista_pacotes[i]
        return lista_pacotes, total_pacotes

    def organize_package(self, txLen, pacote, msg_type, erro_envio = False):

        #Calculo do CRC
        crc16 = crcmod.predefined.Crc('crc-16-mcrf4xx')
        crc16.update(pacote)
        crc = int(crc16.hexdigest())
        
        sub_pacotes, total_pacotes = self.sub_packages(txLen, pacote)

        lista_pacotes = []
        for sub_pacote in sub_pacotes:
            num_pacote = sub_pacotes.index(sub_pacote) + 1
            head = self.tam_padrao(crc, len(sub_pacote), msg_type, num_pacote, total_pacotes, crc)
            print("Head do pacote:", head)
            EOP = bytearray("EOP", "ascii")
            sub_pacote = head+sub_pacote+EOP
            lista_pacotes.append(sub_pacote)

        return lista_pacotes
