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

DOCUMENT_ROOT='documents'

mime_types={
    '.html':'text/html',
    '.txt':'text/plain',
    '.jpg':'image/jpeg',
    '.png':'image/png',
}


while True:
    connected_socket,client_address=s.accept()
    print(f'spojenie s {client_address}')
    pid_chld=os.fork()
    if pid_chld==0:
        s.close()
        f=connected_socket.makefile('rwb')
        while True:
            first=f.readline().decode('ascii').rstrip()
            m=re.match(r'^([^ ]+) +([^ ]+) +([^ ]+) *$',first)
            if m:
                method=m.group(1)
                url=m.group(2)
                protocol=m.group(3)
            else:
                break
            print('method',method)
            print('url',url)
            print('protocol',protocol)
            while True:
                header_in=f.readline().decode('ascii').rstrip()
                if not header_in:
                    break
                print(header_in)
            filename=DOCUMENT_ROOT+url
            try:
                with open(filename,'rb') as ff:
                    response_content=ff.read()
            except FileNotFoundError:
                send_status(f,404,'Not found')
                continue
            base,extension=os.path.splitext(filename)
            if extension in mime_types:
                mime_type=mime_types[extension]
            else:
                mime_type='application/octet-stream'
            f.write('HTTP/1.1 200 OK\r\n'.encode('ascii'))
            f.write(f'Content-type:{mime_type}\r\n'.encode('ascii'))
            response_length=len(response_content)
            f.write(f'Content-length:{response_length}\r\n'.encode('ascii'))
            f.write('\r\n'.encode('ascii'))
            f.write(response_content)
            f.flush()
        print(f'{client_address} uzavrel spojenie')
        sys.exit(0)
    else:
        connected_socket.close()


