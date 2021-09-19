import socket
import os
import sys



def recieveFromClient(port):
    global not_stopped


    SERVER_HOST = '0.0.0.0'
    SERVER_PORT = port
    BuffSize=4000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s = socket.socket()

    SEPARATOR = "-serv"
    try:
        s.bind((SERVER_HOST, SERVER_PORT))
    except:
        sys.stderr.write(f"ERROR: Cannot Bind Host to Port")
        exit(-1)

    s.listen(11)
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
    if len(sys.argv) == 2:
        portNum = int(sys.argv[1])
        if portNum >= 0 and portNum <= 65535:
            while not_stopped:
                recieveFromClient(port=portNum)
        else:
            sys.stderr.write(f"ERROR: Invalid Port Number {portNum}")
            exit(-1)
    else:
        sys.stderr.write(f'ERROR: Invalid Arguments: Usage server-s.py <port-number>')
        exit(-1)
