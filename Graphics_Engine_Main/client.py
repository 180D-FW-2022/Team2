import socket
import json

def client_program():
    #host = socket.gethostname()  # as both code is running on same pc
    host = "131.179.6.151"
    port = 5000  # socket server port number
    print(host)

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    data = {'move': 0}
    data_string = json.dumps(data)

    client_socket.send(data_string.encode())  # send message
    data = client_socket.recv(1024).decode()  # receive response

    print('Received from server: ' + data)  # show in terminal
    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()