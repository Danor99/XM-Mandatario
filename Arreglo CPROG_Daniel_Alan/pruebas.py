import openpyxl
from openpyxl.styles.borders import Border, Side
from openpyxl.styles import PatternFill
#from copy import copy
import pandas as pd
#import pyodbc 
from datetime import datetime, time
from openpyxl import load_workbook
import Utilidades as uti
import os
from tkinter import *
from tkcalendar import*
import Verificacion_CPROG as veri
from Python027 import get027Index       

# df_CPROG = pd.read_excel(r'd:\ambiente\escritorio\NotCode\Arreglo CPROG_Daniel_Alan\05\VACM-CargoCPROG-202305.xlsx', sheet_name = 'CargoCPROG', nrows= 2, usecols = 'B:E', skiprows= range(1,23), header = None)
# df_CPROG.columns = ['A_NombreCorto','CAP','Ing_Dev','CPROG']
# df_CPROG.dropna(axis = 0, inplace = True)

# print(df_CPROG)
# DF_027 = get027Index(date(2023,4,1),'DOROZCO','Xerneas990!')

directorio = r"d:\ambiente\escritorio\NotCode\Arreglo CPROG_Daniel_Alan\05"
directorio_archivos = r"d:\ambiente\escritorio\NotCode\Arreglo CPROG_Daniel_Alan\05"+"\\"

Archivo = "VACM" + "-CargoCPROG-" + str('2023') + str('05') + ".xlsx"

df_CPROG = pd.read_excel(directorio_archivos+Archivo, sheet_name = 'CargoCPROG', nrows= 2, usecols = 'B:E', skiprows= range(1,23), header = None)
df_CPROG.columns = ['A_NombreCorto','CAP','Ing_Dev','CPROG']
df_CPROG.dropna(axis = 0, inplace = True)

print(df_CPROG.iloc[:, 0])