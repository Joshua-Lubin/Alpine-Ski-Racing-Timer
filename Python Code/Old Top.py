#!/usr/bin/python
print('Top started')

import socket
import threading
from datetime import datetime
import psycopg2
from PyQt5 import QtWidgets, QtGui, QtCore, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QLabel, QTableWidget, QTableWidgetItem
import sys

host = ''
port = 23232

global start_time
start_time = []

database_conn = False
database = ''

global race_num
race_num = ''
global last_racers
last_racers = []

def del_racer_1():
    try:
        start_time.pop(0)
        set_race_buttons()
    except:
        print('No racer 1')
def del_racer_2():
    try:
        start_time.pop(1)
        set_race_buttons()
    except:
        print('No racer 2')
def del_racer_3():
    try:
        start_time.pop(2)
        set_race_buttons()
    except:
        print('No racer 3')

class MainWindow(QtWidgets.QMainWindow):
    
    def focus(self):
        self.setFocus()
    
    def __init__(self):
        
        super().__init__()
        
        self.setGeometry(0,0,1280,700)
        self.setWindowTitle("Ski Timer")
        self.setStyleSheet('background-color: #245069; font-size: 30px; color: #ffffff;')
        
        global racer_1
        racer_1 = QPushButton('Racer 1', parent=self)
        racer_1.move(50,50)
        racer_1.setFixedSize(200,200)
        racer_1.clicked.connect(del_racer_1)
        racer_1.setStyleSheet('border-radius: 25px; border-style: none; background-color: #248fd4; color: #ffffff;')
        
        global racer_2
        racer_2 = QPushButton('Racer 2', parent=self)
        racer_2.move(300,50)
        racer_2.setFixedSize(200,200)
        racer_2.setStyleSheet('border-radius: 25px; border-style: none; background-color: #248fd4; color: #ffffff;')
        racer_2.clicked.connect(del_racer_2)
        
        global racer_3
        racer_3 = QPushButton('Racer 3', parent=self)
        racer_3.move(50,300)
        racer_3.setFixedSize(200,200)
        racer_3.setStyleSheet('border-radius: 25px; border-style: none; background-color: #248fd4; color: #ffffff;')
        racer_3.clicked.connect(del_racer_3)

        cancel_label = QLabel('Click racer to cancel', parent=self)
        cancel_label.move(50, 540)
        cancel_label.setFixedSize(450,50)
        cancel_label.setStyleSheet('font-size:40px; font-weight: 600;')
        cancel_label.setAlignment(QtCore.Qt.AlignCenter)
        
        global table
        table = QTableWidget(4, 3, parent=self)
        table.move(600,300)
        table.setFixedSize(630, 200)
        table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        table.setSelectionMode(QtWidgets.QTableWidget.NoSelection)
        table.setHorizontalHeaderLabels("#;Name;Time".split(";"))
        table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        table.horizontalHeader().setSelectionMode(QtWidgets.QTableWidget.NoSelection)
        table.verticalHeader().setSelectionMode(QtWidgets.QTableWidget.NoSelection)
        table.setStyleSheet('background-color: #ffffff; color: #000000; border: 0px; gridline-color: #c2c2c2; font-size: 23px;')
        table.horizontalHeader().setStyleSheet('color: #000000')
        table.verticalHeader().setStyleSheet('color: $000000')
        table.clicked.connect(self.focus)

        table_label = QLabel('Last racers', parent=self)
        table_label.move(600, 540)
        table_label.setFixedSize(630,50)
        table_label.setStyleSheet('font-size:40px; font-weight: 600;')
        table_label.setAlignment(QtCore.Qt.AlignCenter)

        global racer_number
        racer_number = QLabel('Racer #:', parent=self)
        racer_number.move(600, 85)
        racer_number.setFixedSize(630,100)
        racer_number.setStyleSheet('font-size:90px; font-weight: 600;')
        racer_number.setAlignment(QtCore.Qt.AlignLeft)
        
        global connection_label
        connection_label = QLabel('Not Connected', parent=self)
        connection_label.move(1040, 25)
        connection_label.setAlignment(QtCore.Qt.AlignCenter)
        connection_label.setStyleSheet('font-weight: 600; background-color: #db4416; border-radius: 15px;')
        connection_label.setFixedSize(220,60)
        
    def keyPressEvent(self, event):
        if event.key() == 48:
            set_race_num(0)
        if event.key() == 49:
            set_race_num(1)
        if event.key() == 50:
            set_race_num(2)
        if event.key() == 51:
            set_race_num(3)
        if event.key() == 52:
            set_race_num(4)
        if event.key() == 53:
            set_race_num(5)
        if event.key() == 54:
            set_race_num(6)
        if event.key() == 55:
            set_race_num(7)
        if event.key() == 56:
            set_race_num(8)
        if event.key() == 57:
            set_race_num(9)
        if event.key() == 16777219:
            set_race_num('')

app = QApplication(sys.argv)
window = MainWindow()

def set_connection(connection):
    if connection == True:
        connection_label.setStyleSheet('font-weight: 600; background-color: #0dd168; border-radius: 15px;')
        connection_label.setText('Connected')
    else:
        connection_label.setStyleSheet('font-weight: 600; background-color: #db4416; border-radius: 15px;')
        connection_label.setText('Not Connected')

def set_race_buttons():

    b = 0
    
    for x in start_time:
        if not (start_time[b]['num'] == ''):
            if b == 0:
                racer_1.setText('Racer 1: #' + start_time[b]['num'])
                racer_1.setStyleSheet('background-color: #db4416; border-radius: 25px; border-style: none;')
            elif b == 1:
                racer_2.setText('Racer 2: #' + start_time[b]['num'])
                racer_2.setStyleSheet('background-color: #db4416; border-radius: 25px; border-style: none;')
            elif b == 2:
                racer_3.setText('Racer 3: #' + start_time[b]['num'])
                racer_3.setStyleSheet('background-color: #db4416; border-radius: 25px; border-style: none;')
        else:
            if b == 0:
                racer_1.setText('Racer 1')
                racer_1.setStyleSheet('background-color: #db4416; border-radius: 25px; border-style: none;')
            elif b == 1:
                racer_2.setText('Racer 2')
                racer_2.setStyleSheet('background-color: #db4416; border-radius: 25px; border-style: none;')
            elif b == 2:
                racer_3.setText('Racer 3')
                racer_3.setStyleSheet('background-color: #db4416; border-radius: 25px; border-style: none;')
        b = b + 1

    try:
        for y in range(b, 3):
            if y == 0:
                racer_1.setText('Racer 1')
                racer_1.setStyleSheet('border-radius: 25px; border-style: none; background-color: #248fd4;')
            elif y == 1:
                racer_2.setText('Racer 2')
                racer_2.setStyleSheet('border-radius: 25px; border-style: none; background-color: #248fd4;')
            elif y == 2:
                racer_3.setText('Racer 3')
                racer_3.setStyleSheet('border-radius: 25px; border-style: none; background-color: #248fd4;')
    except:
        print('greater than 3 racers')

def set_race_num(racer):
    global race_num
    global racer_number
    if racer == '' and not race_num == '':
        race_num = race_num[:-1]
        racer_number.setText('Racer #: ' + race_num)
    elif not ((race_num == '' and racer == 0) or len(race_num) > 2):
        race_num = race_num + str(racer)
        racer_number.setText('Racer #: ' + race_num)
    else:
        racer_number.setText('Racer #: ' + race_num)
    
def set_table(num, time):
    global last_racers
    
    last_racers.insert(0, [num, time])
    if len(last_racers) > 4:
        last_racers.pop(3)
    z = 0
    for x in last_racers:
        numb = last_racers[z][0]
        tm = last_racers[z][1]
        table.setItem(z,0, QTableWidgetItem(numb))
        table.setItem(z,2, QTableWidgetItem(tm))
        table.resizeColumnToContents(0)
        table.resizeColumnToContents(1)
        print(numb)
        print(tm)
        z = z + 1
    
    
    
while not database_conn:
    try:
        database = psycopg2.connect(user = "postgres",
                                  password = "Facetime2.0",
                                  host = "localhost",
                                  port = "5432",
                                  database = "ski")
        database_conn = True
    except:
        print ("Error while connecting to PostgreSQL")
        
print('connected to database')

def server_listen():
    print('server_listen initiated')
    while True:
        data = master_conn.recv(1024)
        if not data:
            print('Client disconnected')
            set_connection(False)
            break
        else:
            if start_time == []:
                print('No start time')
            else:
                net_time = datetime.now() - start_time[0]['time']
                end_time = datetime.now()
                print(data.decode('utf-8'))
                print('Net time:')
                print(net_time)
                print('Start time:')
                print(start_time[0]['time'])
                print('End time:')
                print(end_time)
                cur = database.cursor()
                
                if start_time[0]['num'] == '':
                    cur.execute("INSERT INTO timer.times (start_time, end_time, net_time) VALUES (%s, %s, %s)", (start_time[0]['time'], end_time, net_time))
                else:
                    cur.execute("INSERT INTO timer.times (number, start_time, end_time, net_time) VALUES (%s, %s, %s, %s)", (start_time[0]['num'], start_time[0]['time'], end_time, net_time))
                
                new_time = str(net_time)
                set_table(start_time[0]['num'], new_time)
                database.commit()
                cur.close()
                start_time.pop(0)
                set_race_buttons()

def server_send():
    print('server_send initiated')
    global start_time
    global race_num
    while True:
        try:
            send = input('Press \'enter\' to send\n')
            master_conn.sendall(b'Received from \'Top\'')
            
            start_time.append({'num': race_num, 'time': datetime.now()})
            
            set_race_buttons()
            race_num = ''
            set_race_num('')
            
            print('Initializing time:')
            print(datetime.now())
        except:
            print('server_send failed')
def create_socket():
    server_send_thread_started = False
    global start_time
    global master_conn
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        while True:
            sock.listen()
            print('listening for connection')
            conn, addr = sock.accept()
            print('connected')
            master_conn = conn
            with master_conn:
                print('Connected with:', addr)
                set_connection(True)

                if not server_send_thread_started:
                    server_send_thread = threading.Thread(target = server_send)
                    server_send_thread.start()
                    server_send_thread_started = True

                server_listen()
                start_time = []

create_socket_thread = threading.Thread(target = create_socket)
create_socket_thread.start()

window.show()
window.setFocus()
sys.exit(app.exec_())