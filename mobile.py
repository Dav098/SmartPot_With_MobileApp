from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivymd.uix.textfield import MDTextField
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.list import OneLineListItem
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import threading
import socket
import os
import shutil
import sqlite3

screen = Screen(name = 'main')
screen2 = Screen(name = 's2')
screen3 = Screen(name = 's3')
screen4 = Screen(name = 's4')
sm = ScreenManager()
error = Label(size_hint =(.5, .15),
                    pos_hint ={'top':.75, 'right':1},
                    color=(0,0,0,1),
                    text ='',
                    )    
        
def download_db(message):
    if(message !='q'):
        try:
            host='192.168.1.8' #client ip
            port = 4005
            
            server = ('192.168.1.3', 4000)
            
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            s.bind((host,port))
            
            s.sendto(message.encode('utf-8'), server)
            file = open("pomiary.db", 'wb')
            data, addr = s.recvfrom(99999)
        
            file.write(bytes(data))
            file.close()
            
            

        except:
            error.text = "Brak połączenia"
            


class data():
    temp_pow = []
    wilg_pow = []
    wilg_gleby = []
    led = []
    n=0
    def load_data():
        path = 'pomiary.db'
        isFile = os.path.isfile(path)
        
        if(isFile==False):
            return('', '', '', '','')
        
        if(isFile==True):
            
            con = sqlite3.connect('pomiary.db')
            cursor = con.cursor()
            cursor.execute("select count(*) from pomiary")
            results = cursor.fetchone()
            data.n=(results[0])
            
            for row in cursor.execute('SELECT temp_pow FROM pomiary'):
                data.temp_pow.append(row)
            
            for row in cursor.execute('SELECT wilg_pow FROM pomiary'):
                data.wilg_pow.append(row)
                
            for row in cursor.execute('SELECT wilg_gleby_d FROM pomiary'):
                data.wilg_gleby.append(row)
                
            for row in cursor.execute('SELECT led FROM pomiary'):
                data.led.append(row)
                
            con.close()
            return (data.n, data.temp_pow, data.wilg_pow, data.wilg_gleby, data.led)
        
def save_config(nazwa_rosliny, min_t_p, max_t_p, min_w_p, max_w_p, min_w_g, max_w_g):
    f = open("plants.txt", "w")
    f.write("nazwa_r{}\n".format(nazwa_rosliny))
    f.write("min_t_p{}\n".format(min_t_p))
    f.write("max_t_p{}\n".format(max_t_p))
    f.write("min_w_p{}\n".format(min_w_p))
    f.write("max_w_p{}\n".format(max_w_p))
    f.write("min_w_g{}\n".format(min_w_g))
    f.write("min_w_g{}\n".format(min_w_g))
    f.close()


def read_config():
    f = open("plants.txt", "r")

    while True:
        lines = f.readline()
        if not lines:
            break

        for i in range(7):
            
            if(lines.strip()[:5]=="nazwa"):
                string = lines.strip()
                MainApp.nazwa_rosliny = (str(string[5:]))
                
            if(lines.strip()[:7]=="min_t_p"):
                string = lines.strip()
                MainApp.min_t_p = (int(string[7:]))
                    
            if(lines.strip()[:7]=="max_t_p"):
                string = lines.strip()
                MainApp.max_t_p = (int(string[7:]))
                
            if(lines.strip()[:7]=="min_w_p"):
                string = lines.strip()
                MainApp.min_w_p = (int(string[7:]))
                    
            if(lines.strip()[:7]=="max_w_p"):
                string = lines.strip()
                MainApp.max_w_p = (int(string[7:]))
                    
            if(lines.strip()[:7]=="min_w_g"):
                string = lines.strip()
                MainApp.min_w_g = (int(string[7:]))
                    
            if(lines.strip()[:7]=="max_w_g"):
                string = lines.strip()
                MainApp.max_w_g = (int(string[7:]))
    f.close()

def save_record(filename):
    src = "pomiary.db"
    isFile = os.path.isfile(src)
    
    if(isFile==True):
        dst =  filename+".db"
        shutil.copyfile(src, dst)

class archiwum():
    temp_pow = []
    wilg_pow = []
    wilg_gleby = []
    led = []
    n=0
    def wybierz(nazwa):
        con = sqlite3.connect(nazwa)
        cursor = con.cursor()
        cursor.execute("select count(*) from pomiary")
        results = cursor.fetchone()
        archiwum.n=(results[0])
        
        for row in cursor.execute('SELECT temp_pow FROM pomiary'):
            archiwum.temp_pow.append(row)
        
        for row in cursor.execute('SELECT wilg_pow FROM pomiary'):
            archiwum.wilg_pow.append(row)
            
        for row in cursor.execute('SELECT wilg_gleby_d FROM pomiary'):
            archiwum.wilg_gleby.append(row)
            
        for row in cursor.execute('SELECT led FROM pomiary'):
            archiwum.led.append(row)
            
        con.close()
        return (archiwum.n, archiwum.temp_pow, archiwum.wilg_pow, archiwum.wilg_gleby, archiwum.led)


con = sqlite3.connect('pomiary.db')
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
                   (temp_pow, wilg_pow, wilg_gleby_d,wilg_gleby_a, led))
    con.commit()
    
def drop_table():
    cursor.execute('''DROP TABLE pomiary''')

class MainApp(MDApp):
    
    nazwa_rosliny=""
    min_t_p = 0
    max_t_p = 0
    min_w_p = 0
    max_w_p = 0
    min_w_g = 0
    max_w_g = 0
    
    def build(self):
        
        (n, temp_pow, wilg_pow, wilg_gleby, led )=(0,'','','','')
        
        
        #funkcja do aktualizacji tabeli
        
        def update_table():
            
            download_db('1') 
            (n, temp_pow, wilg_pow, wilg_gleby, led )=(data.load_data())
            if(temp_pow!=''):
                table.row_data=[
                    (temp_pow[n-i-1][0]+'°C', wilg_pow[n-i-1][0]+'%',  wilg_gleby[n-i-1][0], led[n-i-1][0]) for i in range(n+1)
                    ]
            
            screen.remove_widget(table)
            screen.add_widget(table)
            
            
        def refresh_app(instance):
            isFile = os.path.isfile("pomiary.db")
            
            if(isFile==True):
                read_config()
                update_table()
                note.text = ""
                if((float(data.temp_pow[-1][0])) < MainApp.min_t_p):
                    note.text += "Roslina ma za zimno.\n"
                    
                if((float(data.temp_pow[-1][0])) > MainApp.max_t_p):
                    note.text += "Roslina ma za ciepło.\n"
                    
                if((float(data.wilg_pow[-1][0])) < MainApp.min_w_p):
                    note.text += "Roslina ma za mało wilgotne powietrze.\n"
                    
                if((float(data.wilg_pow[-1][0])) > MainApp.max_w_p):
                    note.text += "Roslina ma za wilgotne powietrze.\n"
                    
                if((float(data.wilg_gleby[-1][0])) < MainApp.min_w_g):
                    note.text += "Roslina ma za mało wody.\n"
                  
                if((float(data.wilg_gleby[-1][0])) > MainApp.max_w_g):
                    note.text += "Roslina ma za dużo wody.\n"
                
                if(data.n>13):
                    if(str(data.led[:12]) == "["+"('Led On',), "*11+"('Led On',)"+"]"):
                        note.text += "Roslina ma za mało swiatła naturalnego"
            
        
       
        def dodaj_rosline(instance):
            dropdown.dismiss()
            sm.switch_to(screen2) 
            
        def zapisz_historie(instance):
            dropdown.dismiss()
            sm.switch_to(screen3) 
            
        def otworz_archiwum(instance):
            dropdown.dismiss()
            sm.switch_to(screen4) 
            
        def reset(instance):
            create_table()
            drop_table()
            create_table()
            insert("0.00", "0", "0","0","0")
            dropdown.dismiss()
        ##########################################################
    
            
        # tworzenie przycisków do wysuwanego menu
        
        dropdown = DropDown()
        
        add = Button(text='Dodaj rosline ręcznie', size_hint_y=None, height=80)
        add.bind(on_press=dodaj_rosline)
        dropdown.add_widget(add)
        
        add = Button(text='Zapisz historię rosliny', size_hint_y=None, height=80)
        add.bind(on_press=zapisz_historie)
        dropdown.add_widget(add)
        
        add = Button(text='Archiwum roslin', size_hint_y=None, height=80)
        add.bind(on_press=otworz_archiwum)
        dropdown.add_widget(add)
        
        add = Button(text='reset aplikacji', size_hint_y=None, height=80)
        add.bind(on_press=reset)
        dropdown.add_widget(add)
        
        

        menu = Button(size_hint =(.4, .1),
                    pos_hint ={'top':.8, 'right':0.8},
                    background_color =(0, 1, 1, 1), 
                    text ="Menu")
        
        menu.bind(on_press=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(menu, 'text', x))
       
        ##########################################################
        
        #przycisk reset
        
        refresh = Button(size_hint =(.2, .1),
                    pos_hint ={'top':.8, 'right':1},
                    background_color =(0, 1, 1, 1), 
                    text ="Refresh")
        
        refresh.bind(on_press=refresh_app)
        
        ##########################################################
        
        #notatka
        anchor = AnchorLayout(anchor_x='left', anchor_y='top')       
        
        note = Label(size_hint =(None, None),
                    pos_hint ={'top':.5, 'left':5},
                    size = (300,200),
                    color=(0,0,0,1),
                    text ='notatka',

                    )
        anchor.add_widget(note)
        
        ##########################################################
        
        
		#tabela z danymi 
        table = MDDataTable(
			pos_hint = {'center_x': 0.5, 'center_y': 0.3},
			size_hint =(0.9, 0.65),
            use_pagination=True,
			column_data = [
				("Temperatura\npowietrza", dp(30)),
				("Wilgotnosc\npowietrza", dp(30)),
				("Wilgotnosc\ngleby", dp(30)),
                ("Swiatło", dp(30))
			],
			row_data = [
				
                # (temp_pow[i], wilg_pow[i], wilg_gleby_d[i], wilg_gleby_a[i], led[i]) for i in range(n)
			]
			)
		
        

        
        
        screen.add_widget(refresh)
        screen.add_widget(error)
        screen.add_widget(anchor) 
        screen.add_widget(menu)
        ##########################################################
        
        ####        ekran do dodawania nowej rosliny
        
        def submit(instance):
            if((min_t_p.text).isnumeric() and (max_t_p.text).isnumeric()
               and (min_w_p.text).isnumeric() and (max_w_p.text).isnumeric() 
               and (min_w_g.text).isnumeric() and (max_w_g.text).isnumeric()):
                save_config(nazwa_rosliny.text, min_t_p.text,
                            max_t_p.text, min_w_p.text, 
                            max_w_p.text, min_w_g.text, max_w_g.text)
                download_db("2")
                sm.switch_to(screen)
        
        def cancel(instance):
            sm.switch_to(screen)
        
        warning = Label(size_hint =(None, None),
                    pos_hint ={'center_x':.5, 'y':.85},
                    size = (300,100),
                    color=(0,0,0,1),
                    text ='Dodanie rosliny powoduje \n usuniecie obecnej bazy danych',

                    )
        screen2.add_widget(warning)
            
        nazwa_rosliny = MDTextField(hint_text="nazwa rosliny", size_hint=(.45, .1), pos_hint={'center_x': .5, 'y': .8})
        screen2.add_widget(nazwa_rosliny)
        
        min_t_p = MDTextField(hint_text="minimalna temperatura powietrza", size_hint=(.45, .1), pos_hint={'center_x': .5, 'y': .7})
        screen2.add_widget(min_t_p)
        
        max_t_p = MDTextField(hint_text="maksymalna temperatura powietrza", size_hint=(.45, .1), pos_hint={'center_x': .5, 'y': .6})
        screen2.add_widget(max_t_p)
        
        min_w_p = MDTextField(hint_text="minimalna wilgotnosc powietrza", size_hint=(.45, .1), pos_hint={'center_x': .5, 'y': .5})
        screen2.add_widget(min_w_p)
        
        max_w_p = MDTextField(hint_text="maksymalna wilgotnosc powietrza", size_hint=(.45, .1), pos_hint={'center_x': .5, 'y': .4})
        screen2.add_widget(max_w_p)
        
        min_w_g = MDTextField(hint_text="minimalna wilgotnosc gleby", size_hint=(.45, .1), pos_hint={'center_x': .5, 'y': .3})
        screen2.add_widget(min_w_g)
        
        max_w_g = MDTextField(hint_text="maksymalna wilgotnosc gleby", size_hint=(.45, .1), pos_hint={'center_x': .5, 'y': .2})
        screen2.add_widget(max_w_g)
        
        btn = Button(text='zapisz', size_hint=(.3, .1), pos_hint={'left': 1, 'y': .05})
        btn.bind(on_press=submit)
        screen2.add_widget(btn)
        btn = Button(text='anuluj', size_hint=(.3, .1), pos_hint={'right': 1, 'y': .05})
        btn.bind(on_press=cancel)
        screen2.add_widget(btn)
        
        ##########################################################
        
        
        ## ekran do zapisu archiwum
        def zapisz_historie_rosliny(instance):
            save_record(str(name.text))
            sm.switch_to(screen)
            
        name = MDTextField(hint_text="Nazwa archiwum", size_hint=(.45, .1), pos_hint={'center_x': .5, 'y': .3})
        screen3.add_widget(name)
        
        btn = Button(text='zapisz', size_hint=(.3, .1), pos_hint={'left': 1, 'y': .05})
        btn.bind(on_press=zapisz_historie_rosliny)
        screen3.add_widget(btn)
        btn = Button(text='anuluj', size_hint=(.3, .1), pos_hint={'right': 1, 'y': .05})
        btn.bind(on_press=cancel)
        screen3.add_widget(btn)
        
        
        ##########################################################
        
        ## ekran do obslugi archiwum
        
        
        
        def cancel(instance):
            screen4.remove_widget(table2)
            sm.switch_to(screen)
            

        
        def setname(instance):
            nazwa = instance.text
            (n, temp_pow, wilg_pow, wilg_gleby, led )=(archiwum.wybierz(nazwa))
            if(temp_pow!=''):
                table2.row_data=[
                    (temp_pow[n-i-1][0]+'°C', wilg_pow[n-i-1][0]+'%',  wilg_gleby[n-i-1][0], led[n-i-1][0]) for i in range(n+1)
                    ]
                
                screen4.add_widget(table2)
                
                
        layout = GridLayout(cols=1, spacing=3, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        path = os.getcwd()
        dir_list = os.listdir(path)
        for file in dir_list:
            if((file[-3:]) == '.db'):
                layout.add_widget(
                    OneLineListItem(text=f"{file}",on_press = setname)
                    )
        root = ScrollView(size_hint=(None, None), size=(400, 200),
            pos_hint={'top':1, 'right':1})
        
        
        
        table2 = MDDataTable(
			pos_hint = {'center_x': 0.5, 'center_y': 0.3},
			size_hint =(0.9, 0.65),
            use_pagination=True,
			column_data = [
				("Temperatura\npowietrza", dp(30)),
				("Wilgotnosc\npowietrza", dp(30)),
				("Wilgotnosc\ngleby", dp(30)),
                ("Swiatło", dp(30))
			],
			row_data = [
				
                # (temp_pow[i], wilg_pow[i], wilg_gleby_d[i], wilg_gleby_a[i], led[i]) for i in range(n)
			]
			)
        
            
        back = Button(size_hint =(.15, .1),
                    pos_hint ={'top':.8, 'left':0.8},
                    background_color =(0, 1, 1, 1), 
                    text ="Powrót")
        
        back.bind(on_press=cancel)
        
        
        root.add_widget(layout)
        screen4.add_widget(root)
        screen4.add_widget(back)
        
        ##################################################
        
        
        sm.add_widget(screen4)
        sm.add_widget(screen3)
        sm.add_widget(screen2)
        sm.add_widget(screen)
        sm.current = 'main'
        return sm
    
    
	
	

if __name__ == '__main__':
    MainApp().run()

