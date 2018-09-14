import socket, pickle, os

def download_status(bytes, tam):
    kbytes = bytes / 1024
    tam_bytes = tam / 1024
    texto = 'Baixando... '
    texto = texto + '{:<.2f}'.format(kbytes) + ' KB '
    texto = texto + 'de ' + '{:<.2f}'.format(tam_bytes) + ' KB'
    print(texto, end="\r")


while True:
    
    try:
        socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketTCP.connect((socket.gethostname(), 8881))
        msg = input("Mensagem: ")

        if msg == 'searchfile':
            socketTCP.send(msg.encode('utf-8'))
            msg = socketTCP.recv(1024)
            print(msg.decode('utf-8'))
            msg = input()
            socketTCP.send(msg.encode('utf-8'))
            msg = socketTCP.recv(1024)
            print (msg.decode('utf-8'))
            
        elif msg == 'endthis':
            socketTCP.send(msg.encode('utf-8'))
            msg = socketTCP.recv(1024)
            print(msg.decode('utf-8'))
            msg = input()
            socketTCP.send(msg.encode('utf-8'))
            msg = socketTCP.recv(1024)
            if msg.decode('utf-8') == 'true':
                break

        elif msg == 'filetransfer':
            socketTCP.send(msg.encode('utf-8'))
            msg = socketTCP.recv(1024)
            print(msg.decode('utf-8'))
            file_name = input()
            socketTCP.send(file_name.encode('utf-8'))
            msg = socketTCP.recv(1024)
            if msg.decode('utf-8') == 'Arquivo não encontrado.':
                print(msg.decode('utf-8'))
            else:
                print(msg.decode('utf-8'))
                file_size = int(socketTCP.recv(80).decode('ascii'))
                if file_size >= 0:
                    print(f'Tamanho do arquivo: {round(file_size/1024,2)}Kb')
                    file = open(file_name, "wb")
                    bytes = socketTCP.recv(1024)
                    soma = len(bytes)
                    while bytes:
                        file.write(bytes)
                        bytes = socketTCP.recv(1024)
                        soma += len(bytes)
                        download_status(soma, int(file_size))
                    file.close()
                    print()
                    print(f'{file_name} recebido.')

        elif msg == 'listdir':
            socketTCP.send(msg.encode('utf-8'))
            while True:
                bytes = socketTCP.recv(4096)
                listdir = pickle.loads(bytes)
                os.system('cls')
                for dir in listdir:
                    print(dir)
                msg = input('>>')
                if msg == 'endlist':
                    socketTCP.send(msg.encode('utf-8'))
                    break
                else:
                    socketTCP.send(msg.encode('utf-8'))

        else:
            socketTCP.send(msg.encode('utf-8'))
            msg = socketTCP.recv(1024)
            print(msg.decode('utf-8'))
        socketTCP.close()
    except Exception as erro:
        print(str(erro))


