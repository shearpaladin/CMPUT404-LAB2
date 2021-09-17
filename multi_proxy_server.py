#!/usr/bin/env python3
import socket
import time
from multiprocessing import Process

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

# handle requests and echo them back to client
def handle_request(addr, conn, proxy_end):
    #recieve data
    full_data = conn.recv(BUFFER_SIZE)
    print(f"Sending recieved data {full_data} to google")
    # Send all data and close connection\
    proxy_end.sendall(full_data)
    # further sends are no longer allowed
    proxy_end.shutdown(socket.SHUT_WR)

    #recieve data and responsd back to client
    data = proxy_end.revc(BUFFER_SIZE)
    print(f"Transferring recieved data {data} to client")
    conn.send(data)


def main():
    extern_host = "www.google.com"
    port = 80

    # create socket, bind, and set to listening mode
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Starting proxy server")
        # allow reused addresses
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)

        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
            print("Connecting to Google")
            remote_ip = get_remote_ip(extern_host)

            #connect to proxy_end
            proxy_end.connect((remote_ip, port))

            p = Process(target=handle_request, args=(addr, conn, proxy_end))
            p.daemon = True
            p.start()
            print("Started process", p)

        conn.close()




if __name__ == "__main__":
    main()
