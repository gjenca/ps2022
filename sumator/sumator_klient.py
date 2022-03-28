#!/usr/bin/env python3
import socket
import sys
import re

def read_reply(f):
    l=f.readline()
    print(f'Server poslal riadok\n{l}',file=sys.stderr)
    l=l.rstrip()
    m=re.match(r'(\d+) (.*)',l)
    if not m:
        print(f'Server poslal divnu odpoved, koncim',file=sys.stderr)
        sys.exit(1)
    status=int(m.group(1))
    status_desc=m.group(2)
    print(f'Server status: {status} {status_desc}')
    if status!=100:
        sys.exit(1)
    reply_content=[]
    while True:
        l=f.readline()
        l=l.strip()
        if not l:
            break
        reply_content.append(l)
    return reply_content

adresa=sys.argv[1]
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((adresa,9999))
f=s.makefile(mode='rw',encoding='utf-8')
verzia=f.readline().rstrip()
if not verzia.endswith('1.0'):
    print(f'Zla verzia protokolu ({verzia})',file=sys.stderr)
    sys.exit(1)
for line in sys.stdin:
    cislo=line.strip()
    f.write(f'CISLO {cislo}\n')
    f.flush()
    reply_content=read_reply(f)
    if reply_content:
        print(f'Neprazdna odpoved na CISLO',file=sys.stderr)
        sys.exit(1)
f.write('SUMA\n')
f.flush()
reply_content=read_reply(f)
if len(reply_content)!=1:
    print(f'Zly obsah odpovede na SUMA',file=sys.stderr)
    sys.exit(1)
print(reply_content[0])
f.flush()



