import socket
import sys

host = sys.argv[1]
port = int(sys.argv[2])
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
client.sendall(b'GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n')
    
try:
    data = client.recv(1024)
    print(data.decode('utf-8'))
except:
    print('Oh noes! %s' % sys.exc_info()[0])
client.close()
sys.exit(0)