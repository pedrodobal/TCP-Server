import socket, psutil, win32api, os, pickle

socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketTCP.bind((socket.gethostname(), 8881))
path = ["C:\\"]
path_cont = 0
listdir = os.listdir(path[0])

def list_dir(subfolder, listdir, path_cont, path):

    if subfolder == "cd.." and path_cont > 0:
        path.pop()
        path_cont -= 1
        listdir = os.listdir(path[path_cont])
    elif subfolder != "cd..":
        path.append(str(path[path_cont] + str(subfolder) + "\\"))
        path_cont += 1
        listdir = os.listdir(path[path_cont])

    return listdir, path_cont, path

def search_file(file_name):
    for drive in win32api.GetLogicalDriveStrings().split('\000')[:-1]:
        for root,dirs,files in os.walk(drive):
            for file in files:
                if file == file_name:
                    return os.path.join(root, file)
    return 'Arquivo não encontrado.'

def loop():

    global path, listdir, path_cont

    while True:
        socketTCP.listen()
        (cliente, addr) = socketTCP.accept()
        msg = cliente.recv(1024)
        msg = msg.decode('utf-8')
        if msg == 'diskfree':
            diskfree = round(psutil.disk_usage('.').free/(1024**3),2)
            diskfree = 'Espaço livre no disco do servidor - '+str(diskfree)+'Gb'
            cliente.send(diskfree.encode('utf-8'))

        elif msg == 'searchfile':
            cliente.send ('Qual arquivo gostaria de pesquisar? '.encode('utf-8'))
            file = cliente.recv(1024)
            cliente.send (search_file(file.decode('utf-8')).encode('utf-8'))

        elif msg == 'endthis':
            cliente.send('Deseja encerrar o servidor? (y/n) '.encode('utf-8'))
            msg = cliente.recv(1024)
            if msg.decode('utf-8') == 'y':
                cliente.send('true'.encode('utf-8'))
                break
            else:
                cliente.send('false'.encode('utf-8'))

        elif msg == 'filetransfer':
            cliente.send('Qual arquivo gostaria de transferir? '.encode('utf-8'))
            msg = cliente.recv(1024)
            file_name = msg.decode('utf-8')
            file_path = search_file(file_name)
            if file_path == 'Arquivo não encontrado.':
                cliente.send(file_path.encode('utf-8'))
            else:
                cliente.send('Arquivo encontrado, iniciando transferencia...'.encode('utf-8'))
                file_size = int(os.stat(file_path).st_size)
                print(file_path)
                print(f'Tamanho do arquivo: {round(file_size/1024,2)}Kb')
                cliente.send(str(file_size).encode('ascii'))
                file = open(file_path, "rb")
                bytes = file.read(1024)
                while bytes:
                    cliente.send(bytes)
                    bytes = file.read(1024)
                cliente.close()
                print(f"{file_name} enviado.")
        elif msg == 'listdir':
            while True:
                bytes = pickle.dumps(listdir)
                cliente.send(bytes)
                msg = cliente.recv(1024)
                if msg.decode('utf-8') == 'endlist':
                    path = ["C:\\"]
                    path_cont = 0
                    listdir = os.listdir(path[0])
                    break
                else:
                    listdir, path_cont, path = list_dir(msg.decode('utf-8'), listdir, path_cont, path)


        else:
            cliente.send('pong'.encode('utf-8'))

        cliente.close()

if __name__=="__main__":
    loop()