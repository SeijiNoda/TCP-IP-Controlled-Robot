import struct, socket, sys, _thread

def get_port():
    return 9001
    
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255',1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    return IP

msg = "alo"
try:
    socket.setdefaulttimeout(0.5)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    sock.connect((get_ip(), get_port()))
    sock.sendall(msg.encode())
finally:
    sock.close()

print('Saindo do socket')