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
        self.head_match = False
        self.pacote_esperado = True

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

    def check_oks(self, pacote,eop_ok):
        pacote2 = pacote
        index_list = []
        try:
            print("Checando Stuffing", len(pacote))
            if pacote2.index(eop_ok) < len(pacote):
                while(1):
                    try:
                        index = pacote2.index(eop_ok)
                        index_list.append(index)
                        pacote2 = pacote[index+len(eop_ok):]
                        print("EOPs repetidos encontrados: ", index_list)
                        if pacote2.index(eop_ok) < len(pacote)-8:
                            continue
                    except Exception as e:
                        return True, index_list
        except Exception as e:
            return False, index_list

    def remove_oks(self, index_list, pacote,string_eop):
        print("Removing Stuffing")
        pacote2 = bytearray(pacote)
        eop_ok = string_eop + bytearray("OK","ascii")

        for index in index_list:
            pacote2[index+len(eop_ok):index+len(eop_ok)] = string_eop
        return pacote2

    def ignore_Stuffing(self, pacote, index_list, string_eop): #Essa função retorna um pacote sem o intervalo em que os Stuffings se encontram
        pacote2 = pacote
        while(1):
            try:
                index = pacote2.index(string_eop)
                index_list.append(index)
                if index in index_list:
                    pacote2 = pacote[index+len(string_eop):]
                    continue
            except Exception as e:
                return index #Retorna o index do eop que não está na lista do repetidos

    def getNData(self):
        """ Read N bytes of data from the reception buffer

        This function blocks until the number of bytes is received
        """
#        temPraLer = self.getBufferLen()
#        print('leu %s ' + str(temPraLer) )

        #if self.getBufferLen() < size:
        #    print("ERROS!!! TERIA DE LER %s E LEU APENAS %s", (size,temPraLer))
        overhead = 0
        x = 10
        PACOTAO = b""
        contagem = 0 #Variável criada pra contar os pacotes e comparar com o valor que está no head
        while(1):
            if len(self.buffer) >= 10:
                print (len(self.buffer))
                start = x
                string_eop = bytearray("EOP", "ascii")
                eop_ok = string_eop + bytearray("OK","ascii")

                package = self.buffer
                head = package[start-10 :start]
                print("Head: ", head)

                crc_head = head[6:]

                head_str = head[5:6] #Definimos que os 2 últimos bytes representam o tamanho (desconsiderando o crc)
                head_str = int.from_bytes(head_str, "big")
                num_pacote = head[0]
                total_pacotes = head[1]
                print("PACOTE", num_pacote, "/", total_pacotes)

                time.sleep(0.05)

                Stuffing, index_list = self.check_oks(package, eop_ok)
                if Stuffing == True:
                    print("Stuffing True")
                    package = self.remove_oks(index_list, package, string_eop)

                print(type(head_str))
                if (head_str + 13) == (len(package[x:])+10): #ANTES ERA 11 POR QUE O HEAD ERA 8, agora é preciso ignorar o começo do buffer pq ele corresponde a outro pacote
                    self.head_match = True
                    print ("Entrou")
                    try:
                        if Stuffing == True:
                            stop = self.ignore_Stuffing(package, index_list, string_eop)
                            while stop == package.index(eop_ok):
                                stop.replace(eop_ok,string_eop)
                                stop = package.index(string_eop)
                        else:
                            stop = package.index(string_eop)
                            print(stop)

                        dados = package[start:stop]

                        crc16 = crcmod.predefined.Crc('crc-16-mcrf4xx')
                        crc16.update(dados)
                        crc = crc16.hexdigest()

                        print("CRC Head: ", crc_head, "CRC Real: ", crc)

                        print("EOP está em: ", stop)
                        print("HEAD: ", head_str)
                        EOP = package[stop:]
                        print("EOP: ", EOP.decode("utf-8"))

                        PACOTAO += dados
                        self.clearBuffer()
                        contagem += 1
                        print("Contagem: ", contagem)
                        print("//////////////////////////")

                        if contagem != num_pacote:
                            print("Pacote diferente do esperado foi recebido")
                            self.pacote_esperado = False
                            break

                        if (num_pacote == total_pacotes):
                            overhead = (len(PACOTAO)/len(PACOTAO)+(13*84)) *100 #Cálculo do overhead
                            break
                        else:
                            continue

                    except Exception as e:
                        print(e)

        return(PACOTAO, overhead, self.pacote_esperado)

    def clearBuffer(self):
        """ Clear the reception buffer
        """
        self.buffer = b""
