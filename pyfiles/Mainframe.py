import pandas as pd
import cx_Oracle
import pyodbc
import sqlite3
import numpy as np
import sqlite3
import os
from tkinter import *
from tkcalendar import*


def CrearDB():
    global Fecha_inicio
    global Fecha_final
    global BUser_Oracle
    global BPassw_Oracle
    Fecha_inicio = Ini_Date.get()
    Fecha_final = Fin_Date.get()
    BUser_Oracle = User_Oracle.get()
    BPassw_Oracle = Passw_Oracle.get()
    

Mainframe=Tk() 
Mainframe.title("Interfaz Informe Mandatario Trimestral LAC") #Titulo de la ventana
Mainframe.iconbitmap("XM-LOGO-RGB-01.ico") #Poner icono
Mainframe.geometry("600x250") #Definir el tamaño de la ventana
Mainframe.resizable(0,0) #Bloquear para que el usuario no la pueda editar
main_title = Label(text="Informe Trimestral LAC",font=("Arial",13)) #Poner titulo dentro de la ventana
main_title.place(x=250,y=20) #Ubicación del texto de las variables de ingreso


Ini_Date_title = Label(text="Fecha inicial del informe",font=("Arial",12)) 
Ini_Date_title.place(x=100,y=50) 
Ini_Date = DateEntry(Mainframe, width=10, background='black', day=1, foreground='white', borderwidth=2, date_pattern='y-mm-dd')
Ini_Date.place(x=100,y=80)

Fin_Date_title = Label(text="Fecha final del informe",font=("Arial",12))
Fin_Date_title.place(x=400,y=50) 
Fin_Date = DateEntry(Mainframe, width=10, background='black', day=1, foreground='white', borderwidth=2, date_pattern='y-mm-dd')
Fin_Date.place(x=400,y=80)


# Realizar textos usuario y contraseña de Oracle
User_Ocle_label=Label(text="Usuario Oracle",font=("Arial",10)) 
User_Ocle_label.place(x=100,y=140)
User_Oracle = Entry(Mainframe)
User_Oracle.place(x=110, y=160)

Passw_Ocle_label=Label(text="Contraseña Oracle",font=("Arial",10)) 
Passw_Ocle_label.place(x=100,y=180)
Passw_Oracle = Entry(Mainframe, show="*")
Passw_Oracle.place(x=110, y=200)

# Sucesos
# Ppales_suc_label=Label(text="Principales sucesos en LAC para el trimestre",font=("Arial",10)) 
# Ppales_suc_label.place(x=30,y=40)
# Ppales_suc = Entry(Mainframe, width = 50)
# Ppales_suc.place(x=30, y=60)

# STR_suc_label=Label(text="Principales sucesos en LAC para el trimestre",font=("Arial",10)) 
# STR_suc_label.place(x=30,y=80)
# STR_suc = Entry(Mainframe, width = 50)
# STR_suc.place(x=30, y=100)

# Boton para ejecutar la funcion 
calcular_btn=Button(Mainframe,text="Crear DB en SQLite",width="30",height="2", command=CrearDB)
calcular_btn.place(x=300,y=150)

Mainframe.mainloop()