import socket
import os
import argparse
import datetime
from pathlib import Path
from socket import *
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-r", help='Root directory for files',  dest = 'OBJECT_DIR' , default='')
parser.add_argument("-p", help='The Port number on which the server will be listening for incoming \
connections',  dest = 'PORT', type=int ,default=8080)


args = parser.parse_args()

object_dir = args.OBJECT_DIR
port = args.PORT


def get_content_type(file_name):

    if file_name.endswith(".jpg") or file_name.endswith(".jpeg"):
        mime_type = 'image/jpg'
    elif file_name.endswith(".png"):
        mime_type = 'image/png'
    elif file_name.endswith(".css"):
        mime_type = 'text/css'
    elif file_name.endswith(".gif"):
        mime_type = 'text/gif'
    elif file_name.endswith(".class"):
        mime_type = 'application/octet-stream'
    elif file_name.endswith(".htm") or file_name.endswith(".html"):
        mime_type = 'text/html'
    else:
        mime_type = 'text/plain'
    return mime_type

HOST,PORT = '192.168.86.242',8080

my_socket = socket(AF_INET,SOCK_STREAM)
my_socket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
my_socket.bind((HOST,PORT))
my_socket.listen(1)

print('Serving on port ' + str(PORT))

while True:
    connection,address = my_socket.accept()
    request = connection.recv(9999999).decode('utf-8')
    string_list = request.split(' ')

    method = string_list[0]
    requesting_file = string_list[1]

    myfile = requesting_file.split('?')[0]
    myfile = myfile.lstrip('/')
    if(myfile == ''):
        myfile = 'index.html'

    try:
        file = open(myfile,'rb')
        response = file.read()
        file.close()

        header = 'HTTP/1.1 200 OK\n'

        file_size = os.path.getsize(myfile)

        header += 'Content-Type: '+ str(get_content_type(myfile)) +'\n'
        header += 'Content-Length: ' + str(file_size) + '\n'
        header += 'Date: ' + str(datetime.datetime.now()) + '\n\n'

    except Exception as e:
        header = 'HTTP/1.1 404 Not Found\n\n'
        response = '<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP Server</p></center></body></html>'.encode('utf-8')

    final_response = header.encode('utf-8')
    final_response += response
    connection.send(final_response)
    connection.close()
