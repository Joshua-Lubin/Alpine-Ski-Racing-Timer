print("Bottom started")

import socket
import threading

host = 'localhost'
port = 23232

start_time = ''
end_time = ''

client_send_thread_started = False
master_s = ''

def client_listen():
    print('client_listen initiated')
    while True:
        data = master_s.recv(1024)
        if not data:
            print('No data')
            break
        else:
            print(data.decode('utf-8'))
    
def client_send():
    print('client_send initiated')
    while True:
        try:
            send = input('Press \'enter\' to send\n')
            master_s.sendall(b'1')
        except:
            print('client_send broken')
            break
connected = False
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5.0)
        socket.setdefaulttimeout(5.0)
        try:
            s.connect((host, port))
            connected = True
            print('Connected')
            
            master_s = s
            
            if not client_send_thread_started:
                client_send_thread = threading.Thread(target = client_send)
                client_send_thread.start()
                client_send_thread_started = True

            client_listen()
        except:
            if connected:
                connected = False
            else:
                print('timed out')
