import socket


def server_program():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print(f'IP address: {ip_address}')
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()
    server_socket.bind((ip_address, port))

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Waiting for connection")
    print("Connection from: " + str(address))

    # receive data stream. it won't accept data packet greater than 1024 bytes
    data = conn.recv(1024).decode()
    print("from connected user: " + str(data))
    
    conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()