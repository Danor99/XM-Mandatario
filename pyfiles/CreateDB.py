import sqlite3
import pandas as pd
import os


try:
    os.remove("variablesDB.db")
except:
    print("No hay base de datos, de que estas hablando")

DbCreationCon = sqlite3.connect('variablesDB.db')

create_sql_STN = "CREATE TABLE IF NOT EXISTS variablesSTN (fecha DATE, ContribucionesConC REAL, FAER REAL, FOES REAL, PRONE REAL, ContribucionesSinC REAL, IPP REAL, IPC REAL, IPPI REAL, TCRM REAL, T_Max REAL, T_Med REAL, T_Min REAL, T_Monomio REAL)"
create_sql_ADDs = "CREATE TABLE IF NOT EXISTS variablesADDS (fecha DATE, NivelTension TEXT, Area TEXT, IngR REAL, IngADD REAL)"
create_sql_STR = "CREATE TABLE IF NOT EXISTS variablesSTR (fecha DATE, IngSTR1 REAL, IngSTR2 REAL)"

DBcursor = DbCreationCon.cursor()
DBcursor.execute(create_sql_ADDs)
DBcursor.execute(create_sql_STN)
DBcursor.execute(create_sql_STR)

DbCreationCon.close()

print('Done CreateDB!')