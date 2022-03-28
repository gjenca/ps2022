#!/usr/bin/env python3
import socket
import os
import sys
import signal
import re

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind(('',9999))
s.listen(5)
signal.signal(signal.SIGCHLD,signal.SIG_IGN)

while True:
    connected_socket,address=s.accept()
    print(f'Spojenie s {address}')
    pid_chld=os.fork()
    if pid_chld==0:
        s.close()
        f=connected_socket.makefile(mode='rw',encoding='utf-8')
        f.write('SUMATOR 1.0\n')
        f.flush()
        n=0
        while True:
            data=f.readline()
            if not data:
                # Klient zavrel spojenie
                break
            # Zmazeme newline a biele znaky na konci
            data=data.rstrip()
            print(data)
            m=re.match(r'CISLO (.*)',data)
            if m:
                status,status_desc=100,'OK'
                content_reply=''
                try:
                    n=n+int(m.group(1))
                except ValueError:
                    status,status_desc=200,'Not a number'
            elif data=='SUMA':
                status,status_desc=100,'OK'
                content_reply=f'{n}\n'
            else:
                status,status_desc=201,'Bad request'
                content_reply=''
            f.write(f'{status} {status_desc}\n')
            f.write(content_reply)
            f.write('\n')
            f.flush()
            if status==201:
                break
        print(f'Koniec spojenia s {address}')
        sys.exit(0)
    else:
        connected_socket.close()

