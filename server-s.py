import socket
import os
import sys
from pickle import GLOBAL



def recieveFromClient(server_name,port):
    global not_stopped

   # global not_stopped = False
    # device's IP address
    host_ip=""
    try:
        host_ip = socket.gethostbyname(server_name)
    except socket.gaierror:
        print("Error while getting host_ip")
    SERVER_HOST = '0.0.0.0'
    SERVER_PORT = port
    BuffSize=4000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    SEPARATOR="-serv"

    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(10)
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
    not_stopped = True

    # if below code is executed, that means the sender is connected
    # need to loop thru clients
    while not_stopped:
        try:
            client_socket, address = s.accept()
            print(f"[+] {address} is connected.")
            # if below code is executed, that means the sender is connected
            # print(f"[+] {address} is connected.")
            #print(f"received::{received}::{filename}::{filesize}")

            msg = "accio\r\n"
            client_socket.send(msg.encode())
            received = client_socket.recv(BuffSize).decode()
            filename, filesize = received.split(SEPARATOR)
            # remove absolute path if there is
            filename = os.path.basename(filename)
            splited = filename.split(".")
            filename = splited[0]+"_server."+splited[1]
            # convert to integer
            filesize = int(float(filesize))
            messagefromClient=""
            with open(filename, "wb") as f:
                while True:
                    # read 1024 bytes from the socket (receive)
                    bytes_read = client_socket.recv(filesize)
                    if not bytes_read:
                        # nothing is received
                        # file transmitting is done
                        break
                    # write to the file the bytes we just received
                    f.write(bytes_read)
                    messagefromClientc = messagefromClient + bytes_read.decode()
                    # update the progress bar
            # close the client socket
            print(f"Message from Client to Server is Recieved. \n\nMessage :: {messagefromClient}::{bytes_read}::{filesize}")
            client_socket.close()
            # close the server socket
            print(f"Message from Client to Server is Recieved. \n\nMessage :: {messagefromClient}::{bytes_read}")
            s.close()
        except:
            sys.stderr.write(f'ERROR: need to put some valiation here')

if __name__ == '__main__':
    global not_stopped
    not_stopped = True
    server_name = ""
    portNum = 0
    if len(sys.argv) == 3:
        server_name = sys.argv[1]
        portNum = int(sys.argv[2])
    else:
        sys.stderr.write(f'ERROR: Invalid Arguments: Usage server-s.py <hostname> <port-number>')
        exit(-1)
    #if sendtoCleint(server_name,port=portNum):
    while not_stopped:
        recieveFromClient(server_name=server_name,port=portNum)