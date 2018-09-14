b = open('img2.png', "rb")
img_file = b.read()
txBuffer = img_file
txLen    = len(txBuffer)

total_pacotes = txLen//128 
if (txLen%128 != 0):
    total_pacotes+=1

n0 = 0
n = 128
p=0
lista_pacotes = []
while(p <= total_pacotes-1):
    lista_pacotes.append(img_file[n0:n])
    n0+=128
    n+=128
    p+=1
lista_pacotes.append(img_file[n:]) 
for i in range(len(lista_pacotes)):
    if lista_pacotes[i] == b"":
        #print(i)
        del lista_pacotes[i]


pacote = b""
for pac in lista_pacotes:
    pacote += pac
#print(len(pacote))
#print(len(img_file))

if pacote == img_file:
    print("certo")
else:
    print("errado")
for i in lista_pacotes:
    if i == b"":
        print("vazio")

#print(total_pacotes)
#print(len(lista_pacotes))
num=1
print(num.to_bytes(2, "big"))