import serial
import sqlite3
import socket
import threading
 
        #baza danych
 
con = sqlite3.connect('pomiary.db', check_same_thread = False)
cursor = con.cursor()
 
def create_table():
    cursor.execute('''CREATE TABLE IF NOT EXISTS pomiary(
                    temp_pow TEXT,
                    wilg_pow TEXT,
                    wilg_gleby_d TEXT,
                    wilg_gleby_a TEXT,
                    led TEXT )''')
    con.commit()
 
def insert(temp_pow, wilg_pow, wilg_gleby_d, wilg_gleby_a, led):
    cursor.execute("INSERT INTO pomiary VALUES (?, ?, ?, ?, ?)",
                   (temp_pow, wilg_pow, wilg_gleby_d, wilg_gleby_a, led))
    con.commit()
 
def drop_table():
    cursor.execute('''DROP TABLE pomiary''')
 
 
        #wysy?anie, otrzymywanie danych
 
temp_pow=""
wilg_pow=""
wilg_gleby_d=""
wilg_gleby_a=""
led=""
koniec=False
host = '192.168.1.3' #Server ip
port = 4000
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
 
 
 
 
def snd_dwn(temp_pow, wilg_pow, wilg_gleby_d, wilg_gleby_a, led):
 
    data, addr = s.recvfrom(1024)
    data = data.decode('utf-8')
    print("Message from: " + str(addr))
    print("From connected user: " + data)      
    if(data == "2"):
        drop_table()
        create_table()
 
    print("Sending...")
    file = open("pomiary.db", 'rb')
    filedata = file.read(99999)
    s.sendto(bytes(filedata), addr)
 
 
 
class download(threading.Thread):
    def __init__(self, temp_pow, wilg_pow, wilg_gleby_d, wilg_gleby_a, led):
        threading.Thread.__init__(self)
        self.temp_pow = temp_pow
        self.wilg_pow = wilg_pow
        self.wilg_gleby_d = wilg_gleby_d
        self.wilg_gleby_a = wilg_gleby_a
        self.led = led
    def run(self):
        snd_dwn(self.temp_pow, self.wilg_pow, self.wilg_gleby_d, self.wilg_gleby_a, self.led)
        print("Wys?ano")
 
 
 
        #g?�wna cz??? kodu
 
print("Server Started")
create_table()
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=0.01)
 
while True:
    data_arduino = str(arduino.readline())
 
    if data_arduino!="b''":                     #odczytuj?c dane z konsoli otrzymujemy: b'(tresc)'
        data_arduino = (data_arduino[2:-1])     # wiec pomijamy niechciane znaki
        print(data_arduino) 
        if data_arduino[0] == 't':
            temp_pow = data_arduino[1:]
        if data_arduino[0] == 'h':
            wilg_pow = data_arduino[1:]
        if data_arduino[0] == 'd':
            wilg_gleby_d = data_arduino[1:]
        if data_arduino[0] == 'a':
            wilg_gleby_a = data_arduino[1:]
        if data_arduino[0] == 'L':
            led = data_arduino[1:]
            koniec = True
 
 
        if koniec == True:
            insert(temp_pow, wilg_pow, wilg_gleby_d, wilg_gleby_a, led)
            koniec = False
 
            #wysylanie i odbieranie danych od klienta
            download(temp_pow, wilg_pow, wilg_gleby_d, wilg_gleby_a, led).start()
 
            for row in cursor.execute('SELECT * FROM pomiary'):
                print(row)
 
c.close()