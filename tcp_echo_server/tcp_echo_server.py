#!/usr/bin/env python3
import socket
import os
import sys
import signal

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind(('',9999))
s.listen(5)
signal.signal(signal.SIGCHLD,signal.SIG_IGN)

while True:
    connected_socket,client_address=s.accept()
    print(f'spojenie s {client_address}')
    pid_chld=os.fork()
    if pid_chld==0:
        s.close()
        while True:
            bs=connected_socket.recv(1024)
            if not bs:
                break
            print('data prijate\n')
            connected_socket.send(b'PONG'+bs)
        print(f'{client_address} uzavrel spojenie')
        sys.exit(0)
    else:
        connected_socket.close()


