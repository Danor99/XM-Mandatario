import pandas as pd
import cx_Oracle
import pyodbc
import sqlite3
import numpy as np
import sqlite3
import os
from tkinter import *

## Interfaz para analistas

def CrearDB():
    global Fecha_inicio
    global Fecha_final
    global BUser_Oracle
    global BPassw_Oracle
    BUser_Oracle = User_Oracle.get()
    BPassw_Oracle = Passw_Oracle.get()
    Mainframe.destroy()
    

Mainframe=Tk() 
Mainframe.title("Interfaz Informe Mandatario Trimestral LAC") #Titulo de la ventana
Mainframe.iconbitmap("XM-LOGO-RGB-01.ico") #Poner icono
Mainframe.geometry("600x150") #Definir el tamaño de la ventana
Mainframe.resizable(0,0) #Bloquear para que el usuario no la pueda editar

main_title = Label(text="Conexion BD y Creación SQLite",font=("Arial",13)) #Poner titulo dentro de la ventana
main_title.place(x=175,y=20) #Ubicación del texto de las variables de ingreso


# Realizar textos usuario y contraseña de Oracle
User_Ocle_label=Label(text="Usuario Oracle",font=("Arial",10)) 
User_Ocle_label.place(x=50,y=50)
User_Oracle = Entry(Mainframe)
User_Oracle.place(x=60, y=70)

Passw_Ocle_label=Label(text="Contraseña Oracle",font=("Arial",10)) 
Passw_Ocle_label.place(x=50,y=90)
Passw_Oracle = Entry(Mainframe, show="*")
Passw_Oracle.place(x=60, y=110)

# Boton para ejecutar la funcion 
calcular_btn=Button(Mainframe,text="Crear DB en SQLite",width="30",height="2", command=CrearDB)
calcular_btn.place(x=300,y=60)

Mainframe.mainloop()

print("Done Interfaz Oracle!")

## Conexion SQL - Alan
class ConexionSQL(object):
    def __init__(self, server, port, database, driver='SQL Server'):
        self.database = database
        self.server = server
        self.port = port
        self.driver = "{"+driver+"}"
        self.con_str = f"DRIVER={self.driver};SERVER={self.server},{self.port};Database={self.database};Applicationintent=READONLY;Trusted_Connection=Yes"

    def consultar(self, query:str, params=None):
        with pyodbc.connect(self.con_str) as cnxn:
            cursor=cnxn.cursor()
            cursor.execute(query)
            lista = cursor.fetchall()
            fields = [x[0] for x in cursor.description]
            df = pd.DataFrame.from_records(lista, columns=fields)
        return df
    
def conCarperQuery(path):
    scriptfile = open(path, 'r')
    querySQL = scriptfile.read()
    df = STRcon.consultar(querySQL)
    return df

def conMidQuery(path):
    scriptfile = open(path, 'r')
    querySQL = scriptfile.read()
    df = ADDcon.consultar(querySQL)
    return df

def conCalQuery(path):
    scriptfile = open(path, 'r')
    querySQL = scriptfile.read()
    df = CALcon.consultar(querySQL)
    return df

## Conexion a ADDs - SDL - AAux
ServerNameSQLADD = 'COMEDxmV144'
PortMidADD = '3052'
DataBaseMid = 'BDMIDXM'

ADDcon=ConexionSQL(ServerNameSQLADD, PortMidADD, DataBaseMid)

addsdf = conMidQuery(r"d:\ambiente\escritorio\NotCode\Querys\QueryADDs.sql")
sdldf = conMidQuery(r"d:\ambiente\escritorio\NotCode\Querys\CargosSDL.sql")
aauxdf = conMidQuery(r"d:\ambiente\escritorio\NotCode\Querys\AreasAux.sql")

## Conexion para Convocatorias STN (MID)
CONVcon=ConexionSQL(ServerNameSQLADD, PortMidADD, DataBaseMid)

CONVDF = conMidQuery(r"d:\ambiente\escritorio\NotCode\Querys\ConvocatoriasSTN.sql")

## Conexion a STR - CPROG
ServerNameSQLSTR = 'COMEDxmV323'
PortMidSTR = '3052'
DataBaseSTR = 'BDCargosPerdLAC'

STRcon=ConexionSQL(ServerNameSQLSTR, PortMidSTR, DataBaseSTR)

strdf_Ing1 = conCarperQuery(r"d:\ambiente\escritorio\NotCode\Querys\QuerySTR1.sql")
strdf_Ing2 = conCarperQuery(r"d:\ambiente\escritorio\NotCode\Querys\QuerySTR2.sql")
strdf_carp1 = conCarperQuery(r"d:\ambiente\escritorio\NotCode\Querys\CarperSTR1.sql")
strdf_carp2 = conCarperQuery(r"d:\ambiente\escritorio\NotCode\Querys\CarperSTR2.sql")
sdl_carp = conCarperQuery(r"d:\ambiente\escritorio\NotCode\Querys\CargosSDL2.sql")
cprogdf = conCarperQuery(r"d:\ambiente\escritorio\NotCode\Querys\CPROG.sql")

## Conexion a Calidad SDL
ServerNameSQLCal = 'COMEDxmV165'
PortCal = '3052'
DataBaseCal = 'BDSDL'

CALcon=ConexionSQL(ServerNameSQLCal, PortCal, DataBaseCal)

calidaddf = conCalQuery(r"d:\ambiente\escritorio\NotCode\Querys\IndicadoresPaisCal.sql")


## Conexion STN
# My Data
host = 'dom1-P8-scan.xm.com.co'
port = '5458'
service_name = 'PDN18'
user = BUser_Oracle
password = BPassw_Oracle

# Server Data Concatenation
dsn_tns = cx_Oracle.makedsn(host = host, port = port, service_name = service_name) 
conn = cx_Oracle.connect(user= user, password=password, dsn=dsn_tns) 

# Query Contribuciones
queryOR_Contribuciones = open(r"Querys\Contribuciones.sql",'r').read()
ContribucionesDF = pd.read_sql(sql=queryOR_Contribuciones, con=conn)

# Query Balance Cargos
queryOR_Balance_cargos = open(r"Querys\Balance_cargos.sql",'r').read()
Balance_cargosDF = pd.read_sql(sql=queryOR_Balance_cargos, con=conn)

# Query CargosSTN
queryOR_CargosSTN = open(r"Querys\CargosSTN.sql",'r').read()
Cargos_STNDF = pd.read_sql(sql=queryOR_CargosSTN, con=conn)

# Query Demanda STN
queryOR_DemandaSTN = open(r"Querys\DemandaSTN.sql",'r').read()
DemandaSTN_DF = pd.read_sql(sql=queryOR_DemandaSTN, con=conn)

# Query IPPyTCRM
queryOR_IPPyTCRM = open(r"Querys\IPPyTCRM.sql",'r').read()
IPP_y_TCRMDF = pd.read_sql(sql=queryOR_IPPyTCRM, con=conn)

# Query IPPI
queryOR_IPPI = open(r"Querys\IPPI.sql",'r').read()
IPPI_DF = pd.read_sql(sql=queryOR_IPPI, con=conn)

# Query IPC
queryOR_IPC = open(r"Querys\IPC.sql",'r').read()
IPC_DF = pd.read_sql(sql=queryOR_IPC, con=conn)

conn.close()
print('Done Connections!')

## CreateDB SQLite
try:
    os.remove("variablesDB.db")
except:
    print("No hay base de datos, de que estas hablando")

DbCreationCon = sqlite3.connect('variablesDB.db')

create_sql_STN = "CREATE TABLE IF NOT EXISTS variablesSTN (fecha DATE, ContribucionesConC REAL, FAER REAL, FOES REAL, PRONE REAL, ContribucionesSinC REAL, IPP REAL, IPC REAL, IPPI REAL, TCRM REAL, T_Max REAL, T_Med REAL, T_Min REAL, T_Monomio REAL, Demanda_STN REAL)"
create_sql_ADDs = "CREATE TABLE IF NOT EXISTS variablesADDS (fecha DATE, NivelTension TEXT, Area TEXT, IngR REAL, IngADD REAL)"
create_sql_STR = "CREATE TABLE IF NOT EXISTS variablesSTR (fecha DATE, IngSTR1 REAL, IngSTR2 REAL, CD4STR1, DemandaSTR1, DT4STR1, CD4STR2, DemandaSTR2, DT4STR2)"
create_sql_CONV = "CREATE TABLE IF NOT EXISTS convocatoriasSTN (Convocatoria TEXT, FechaInicial DATE, FechaFinal DATE, NAnualidad TEXT, Nombre TEXT, Descripcion TEXT, Resolucion TEXT)"
create_sql_SDL = "CREATE TABLE IF NOT EXISTS variablesSDL (fecha DATE, Area TEXT, Mercado TEXT, NT TEXT, DtUN REAL, DT REAL)"
create_sql_SDL2 = "CREATE TABLE IF NOT EXISTS variablesSDL2 (fecha DATE, Tipo TEXT, MercadoID TEXT, Mercado TEXT, Comercializador TEXT, DT1 REAL, DT2 REAL, DT3 REAL, EnergiaLiqN1 REAL, EnergiaLiqN2 REAL, EnergiaLiqN3 REAL, CargoLiqN1 REAL, CargoLiqN2 REAL, CargoLiqN3 REAL )"
create_sql_CPROG = "CREATE TABLE IF NOT EXISTS variablesCPROG (fecha DATE, Mercado TEXT, MercadoID TEXT, CPROG REAL)"
create_sql_CALIDAD = "CREATE TABLE IF NOT EXISTS variablesCALIDAD (fecha DATE, SAIDI REAL, SAIFI REAL)"


DBcursor = DbCreationCon.cursor()
DBcursor.execute(create_sql_ADDs)
DBcursor.execute(create_sql_STN)
DBcursor.execute(create_sql_STR)
DBcursor.execute(create_sql_CONV)
DBcursor.execute(create_sql_SDL)
DBcursor.execute(create_sql_SDL2)
DBcursor.execute(create_sql_CPROG)
DBcursor.execute(create_sql_CALIDAD)


DbCreationCon.close()

print('Done CreateDB!')

## ConstructorSQLite
# Proceso STN
STNbigDF = IPP_y_TCRMDF.merge(ContribucionesDF,on="FECHA").merge(Balance_cargosDF,on="FECHA").merge(IPPI_DF, on= "FECHA").merge(IPC_DF, on= "FECHA").merge(Cargos_STNDF, left_on= "FECHA", right_on = "FECHINIC").merge(DemandaSTN_DF, left_on= "FECHA", right_on="FECHINIC")
STNbigDF["CONTRIBUCIONES1"] = abs(STNbigDF["TRANSMISORES"])
STNbigDF["CONTRIBUCIONES2"] = STNbigDF["CONTRIBUCIONES1"] - STNbigDF["FAER"] - STNbigDF["FOES"] - STNbigDF["PRONE"]
STNDF = STNbigDF[["FECHA","CONTRIBUCIONES1","FAER","FOES","PRONE","CONTRIBUCIONES2", "IPP", "IPC", "IPPI", "TCRM", "T_NETO_MAXIMA", "T_NETO_MEDIA", "T_NETO_MINIMA", "T_NETO_MONOMIO", "DEMANDA_STN"]]

# Proceso ADDs
ADDDF = addsdf[["Fecha", "NT","ADD","IngR","IngADD"]]

# Proceso STR
STRDF = strdf_Ing1.merge(strdf_Ing2, on="fechaTrabajo").merge(strdf_carp1, on="fechaTrabajo").merge(strdf_carp2, on="fechaTrabajo")

# Proceso CPROG
CPROGDF = cprogdf.merge(aauxdf, on="MercadoID")

SDLDF = sdldf
SDLDF2 = sdl_carp.merge(aauxdf, on="MercadoID")
CALIDAD = calidaddf

finalconn = sqlite3.connect('variablesDB.db')
finalCursor = finalconn.cursor()

for row in STNDF.itertuples():
    insert_sql_STN = f"INSERT INTO variablesSTN (fecha, ContribucionesConC, FAER, FOES, PRONE, ContribucionesSinC, IPP, IPC, IPPI, TCRM, T_Max, T_Med, T_Min, T_Monomio, Demanda_STN) VALUES ('{row[1]}', {row[2]}, {row[3]}, {row[4]}, {row[5]}, {row[6]}, {row[7]}, {row[8]}, {row[9]}, {row[10]}, {row[11]}, {row[12]}, {row[13]}, {row[14]}, {row[15]})"
    finalCursor.execute(insert_sql_STN)

for row in ADDDF.itertuples():
    insert_sql_ADDs = f"INSERT INTO variablesADDs (fecha, NivelTension, Area, IngR, IngADD) VALUES ('{row[1]}', '{row[2]}', '{row[3]}', {row[4]}, {row[5]})"
    finalCursor.execute(insert_sql_ADDs)

for row in STRDF.itertuples():
    insert_sql_STR = f"INSERT INTO variablesSTR (fecha, IngSTR1, IngSTR2, CD4STR1, DemandaSTR1, DT4STR1, CD4STR2, DemandaSTR2, DT4STR2) VALUES ('{row[1]}', {row[2]}, {row[3]}, {row[4]}, {row[5]}, {row[6]}, {row[7]}, {row[8]}, {row[9]})"
    finalCursor.execute(insert_sql_STR)

for row in CONVDF.itertuples():
    insert_sql_CONV = f"INSERT INTO convocatoriasSTN (Convocatoria, FechaInicial, FechaFinal, NAnualidad, Nombre, Descripcion, Resolucion) VALUES ('{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}', '{row[5]}', '{row[6]}', '{row[7]}')"
    finalCursor.execute(insert_sql_CONV)

for row in SDLDF.itertuples():
    insert_sql_SDL = f"INSERT INTO variablesSDL (fecha, Area, Mercado, NT, DtUN, DT) VALUES ('{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}', {row[5]}, {row[6]})"
    finalCursor.execute(insert_sql_SDL)

for row in SDLDF2.itertuples():
    insert_sql_SDL2 = f"INSERT INTO variablesSDL2 (fecha, Tipo, MercadoID, Comercializador, DT1, DT2, DT3, EnergiaLiqN1, EnergiaLiqN2, EnergiaLiqN3, CargoLiqN1, CargoLiqN2, CargoLiqN3, Mercado) VALUES ('{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}', {row[5]}, {row[6]}, {row[7]}, {row[8]}, {row[9]}, {row[10]}, {row[11]}, {row[12]}, {row[13]}, '{row[14]}')"
    finalCursor.execute(insert_sql_SDL2)

for row in CPROGDF.itertuples():
    insert_sql_CPROG = f"INSERT INTO variablesCPROG (fecha, MercadoID, CPROG, Mercado) VALUES ('{row[1]}', '{row[2]}', {row[3]}, '{row[4]}')"
    finalCursor.execute(insert_sql_CPROG)

for row in CALIDAD.itertuples():
    insert_sql_CALIDAD = f"INSERT INTO variablesCALIDAD (fecha, SAIDI, SAIFI) VALUES ('{row[1]}', {row[2]}, {row[3]})"
    finalCursor.execute(insert_sql_CALIDAD)

finalconn.commit()

print('Done ConstructorSQLite!')



