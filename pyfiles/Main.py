# -*- coding: utf-8 -*-

# Plantilla informe mandatario trimestral 
#
# El siguiente programa genera el informe trimestral del grupo LAC por medio de las bases de datos de ORACLE
# y SQL DM, almacenadas en la DB interna y analizadas por medio de matplotlib.
# 
#
# Realizado por: Daniel Orozco Restrepo - Danor
# Codigo = 65576
# Fecha de la 1.0: 23/05/2023
#
# 1. FUNCIONES AUXILIARES
# 2. Interfaz de usuario
# 3. Indicadores
# 4. STN
# 5. STR
# 6. ADDs
# 7. Convocatorias STN y STR
# 8. SDL
# 9. CPROG
# 10. Calidad SDL
# 11. Analisis STN


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import calendar
import math
import datetime as datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta
from tkinter import *
from tkcalendar import*
from tqdm import tqdm
tqdm.pandas()



## Conexion a SQLite y extraccion de las 4 bases de datos
con = sqlite3.connect("variablesDB.db")

# Maximos regisros disponibles en SQLite o base de datos local
strdf = pd.read_sql_query("SELECT * FROM variablesSTR", con)
stndf = pd.read_sql_query("SELECT * FROM variablesSTN", con)
addsdf = pd.read_sql_query("SELECT * FROM variablesADDS", con)
convdf = pd.read_sql_query("SELECT * FROM convocatoriasSTN", con)
sdldf = pd.read_sql_query("SELECT * FROM variablesSDL", con)
sdldfsinADD = pd.read_sql_query("SELECT * FROM variablesSDL2", con)
cprogdf = pd.read_sql_query("SELECT * FROM variablesCPROG", con)
calidaddf = pd.read_sql_query("SELECT * FROM variablesCALIDAD", con)

con.close()

print("Registros disponibles del STN hasta " + str(stndf["fecha"][0]))
print("Registros disponibles del STR hasta " + str(strdf["fecha"][0]))
print("Registros disponibles de ADDs hasta " + str(addsdf["fecha"][0]))
print("Registros disponibles de SDL hasta " + str(sdldf["fecha"][0]))
print("Registros disponibles de Calidad SDL hasta " + str(calidaddf["fecha"][0]))
print("Registros disponibles de CPROG hasta " + str(cprogdf["fecha"][0]))

## Functions

def format(Valor):
    return int("{:10.0f}".format(Valor))

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

def prep_df(df):
    df["fecha"] = pd.to_datetime(df["fecha"])
    df["Mes"]= df["fecha"].dt.month_name(locale='Spanish')
    df["Año"]= df["fecha"].dt.year
    return df

# Solo df's con int como indice.
def get_meses_trimestre(df):
    mesesLista = df.head(3).index.tolist()
    if mesesLista == ['Enero','Febrero','Marzo']:
        trimestre = 'primer trimestre'
    elif mesesLista == ['Abril','Mayo','Junio']:
        trimestre = 'segundo trimestre'
    elif mesesLista == ['Julio','Agosto','Septiembre']:
        trimestre = 'tercer trimestre'
    elif mesesLista == ['Octubre','Noviembre','Diciembre']:
        trimestre = 'cuarto trimestre'
    else:
        trimestre = 'indefinido'
    return trimestre


def get_año(df):
    Año = str(int(df.loc[0]['Año']))
    return Año

def get_graficaDF(df, colName, rowN = 3):
    GraficaDF = df.head(rowN).sort_values("fecha")[["Mes", colName]].set_index(["Mes"])
    return GraficaDF

def unique(list1):
    list_set = set(list1)
    unique_list = (list(list_set))
    for x in unique_list:
        return x

def add_months(start_date, delta_period):
  end_date = start_date + relativedelta(months=delta_period)
  return end_date

# Funcion de graficas STN y STR
def realizar_grafica(GraficaDF, name = "SinNombre", title = 'Sin titulo', tamañoFig = (6,4), tipoG = 'none'):
    # Eje para graifcar grafica en barras
    ax = GraficaDF.plot.bar(rot=0, color = ['#440099', '#FF6A13', '#75787B'], figsize = tamañoFig)
    if len(GraficaDF.columns) > 1:
        # Hallar maximo absoluto del DF
        max_value = GraficaDF.max().max()
        min_value = GraficaDF.min().min()
    else:
        # Hallar minimo absoluto del DF
        max_value = GraficaDF.max()
        min_value = GraficaDF.min()
    
    # Valores para ajuste de ejes
    scale = max_value*0.1
    den = 1000000000
    
    # Ajuste de formato para DF´s con cifras muy grandes
    ndecimales = math.log(max_value,10) * -1 # Logaritmo en base 10 para obtener numero de decimales
    tickPpal = int(round_up(max_value,round(ndecimales,0))) # Ajustar el ultimo cero para obtener graficas con mayor zoom a los valores
    ytick_val = [tickPpal*0.2, tickPpal*0.4, tickPpal*0.6, tickPpal*0.8, tickPpal] # Valores base para los valores de eje y en grafica
    tick_lab2 = list(map(lambda x: int(x/den), ytick_val)) 
    ytick_lab = list(map(lambda x: str(x) + 'milM', tick_lab2))

    # Contribuciones tiene el tickPpal al 1 en los decimales dado que varia bastante entre trimestres
    if tipoG == 'Contribuciones':
        ajuste_dis_FOES = [-0.25,0.75,1.75] # Posicion de los marcadores para cada columna en el eje X (no varia)
        ajuste_dis_PRONE = [-0.09,0.91,1.91]
        ajuste_dis_FAER = [0.09,1.09,2.09]
        tickPpal = int(round_up(max_value,round(ndecimales,1)))
        for idx in range(len(GraficaDF)):
            ax.text(ajuste_dis_FOES[idx], GraficaDF['FOES'][idx] + scale*0.05 , round(GraficaDF['FOES'][idx]/den,1), size = 9) # Posicion de los marcadores para cada columna en el eje Y (si varia)
            ax.text(ajuste_dis_PRONE[idx], GraficaDF['PRONE'][idx] + scale*0.05 , round(GraficaDF['PRONE'][idx]/den,1), size = 9)
            ax.text(ajuste_dis_FAER[idx], GraficaDF['FAER'][idx] + scale*0.05 , round(GraficaDF['FAER'][idx]/den,1), size = 9)
        ytick_val = [tickPpal*0.7, tickPpal*0.8, tickPpal*0.9, tickPpal]
        tick_lab2 = list(map(lambda x: int(x/den), ytick_val))
        ytick_lab = list(map(lambda x: str(x) + 'milM', tick_lab2))
        plt.ylim(tickPpal*0.7, tickPpal*1.05) # Limite de vista en la grafica para el eje Y (para hacer las graficas mas pequeñas y las barras menos largas)

    if tipoG == 'Ingresos STN':
        ajuste_dis_1 = [-0.25,0.75,1.75]
        ajuste_dis_2 = [0,1,2]
        for idx in range(len(GraficaDF)):
            ax.text(ajuste_dis_1[idx], GraficaDF["Ingreso Neto Sin Contribuciones"][idx] + scale*0.1, round(GraficaDF["Ingreso Neto Sin Contribuciones"][idx]/den,1), size = 9)
            ax.text(ajuste_dis_2[idx], GraficaDF["Ingreso Neto Con Contribuciones"][idx] + scale*0.1, round(GraficaDF["Ingreso Neto Con Contribuciones"][idx]/den,1), size = 9)
        ytick_val = [tickPpal*0.25, tickPpal*0.3, tickPpal*0.35]
        tick_lab2 = list(map(lambda x: int(x/den), ytick_val))
        ytick_lab = list(map(lambda x: str(x) + 'milM', tick_lab2))
        plt.ylim(tickPpal*0.3, tickPpal*0.37)

    
    if tipoG == 'Demanda STN':
        ajuste_dis_1 = [-0.1,0.9,1.9]
        for idx in range(len(GraficaDF)):
            ax.text(ajuste_dis_1[idx], GraficaDF["Demanda STN"][idx] + scale*0.1, round(GraficaDF["Demanda STN"][idx]/den,2), size = 10)
        ytick_val = [tickPpal*0.6, tickPpal*0.625, tickPpal*0.65, tickPpal*0.675]
        tick_lab2 = list(map(lambda x: round(x/den, 2), ytick_val))
        ytick_lab = list(map(lambda x: str(x) + 'milM', tick_lab2))
        plt.ylim(tickPpal*0.57, tickPpal*0.65)

    if tipoG == 'Ingresos STR':
        ajuste_dis_1 = [-0.25,0.75,1.75]
        ajuste_dis_2 = [0,1,2]
        for idx in range(len(GraficaDF)):
            ax.text(ajuste_dis_1[idx], GraficaDF["Ing STR Norte"][idx] + scale*0.2, round(GraficaDF["Ing STR Norte"][idx]/den,1), size = 10)
            ax.text(ajuste_dis_2[idx], GraficaDF["Ing STR Centro Sur"][idx] + scale*0.2, round(GraficaDF["Ing STR Centro Sur"][idx]/den,1), size = 10)

    if tipoG == 'Demanda STR':
        ajuste_dis_1 = [-0.20,0.8,1.8]
        ajuste_dis_2 = [0.07,1.07,2.07]
        for idx in range(len(GraficaDF)):
            ax.text(ajuste_dis_1[idx], GraficaDF["Demanda STR Norte"][idx] + scale*0.5, round(GraficaDF["Demanda STR Norte"][idx]/den,1), size = 10)
            ax.text(ajuste_dis_2[idx], GraficaDF["Demanda STR Centro Sur"][idx] + scale*0.5, round(GraficaDF["Demanda STR Centro Sur"][idx]/den,1), size = 10)
        ytick_val = [tickPpal*0.2, tickPpal*0.3, tickPpal*0.4, tickPpal*0.5]
        tick_lab2 = list(map(lambda x: int(x/den), ytick_val))
        ytick_lab = list(map(lambda x: str(x) + 'milM', tick_lab2))
        plt.ylim(tickPpal*0.1, tickPpal*0.55)

    
    plt.yticks(ytick_val, ytick_lab) # Aplicar a cada label la posicion que le corresponde = value
    plt.title(title)
    save = plt.savefig(r"Temp\{name}.png".format(name=name)) # Se guarda cada grafica en la carpeta de Temp
    return save


#### ----------------- DESACTIVADA INTEFAZ HASTA ENTRAR EN PRODUCCIÓN -------------------------
# def getFechas():
#     global Fecha_inicio
#     global Fecha_final
#     Fecha_inicio = Ini_Date.get()
#     Fecha_final = Fin_Date.get()
#     Mainframe.destroy()

# ## Interfaz Fecha a seleccionar:

# Mainframe=Tk() 
# Mainframe.title("Interfaz Informe Mandatario Trimestral LAC") #Titulo de la ventana
# Mainframe.iconbitmap("XM-LOGO-RGB-01.ico") #Poner icono
# Mainframe.geometry("600x250") #Definir el tamaño de la ventana
# Mainframe.resizable(0,0) #Bloquear para que el usuario no la pueda editar

# main_title = Label(text="Seleccion Fechas Mandatario",font=("Arial",13)) #Poner titulo dentro de la ventana
# main_title.place(x=175,y=20) #Ubicación del texto de las variables de ingreso

# Ini_Date_title = Label(text="Fecha inicial del informe",font=("Arial",12)) 
# Ini_Date_title.place(x=50,y=60) 
# Ini_Date = DateEntry(Mainframe, width=10, background='black', day=1, foreground='white', borderwidth=2, date_pattern='y-mm-dd')
# Ini_Date.place(x=50,y=90)

# Fin_Date_title = Label(text="Fecha final del informe",font=("Arial",12))
# Fin_Date_title.place(x=350,y=60) 
# Fin_Date = DateEntry(Mainframe, width=10, background='black', day=1, foreground='white', borderwidth=2, date_pattern='y-mm-dd')
# Fin_Date.place(x=350,y=90)

# # Boton para ejecutar la funcion 
# calcular_btn=Button(Mainframe,text="Filtrar Fecha",width="30",height="2", command=getFechas)
# calcular_btn.place(x=150,y=150)

# Mainframe.mainloop()

## Variables Iniciales

plt.rcParams.update({'figure.max_open_warning': 0}) # Necesario para graficar tantas cosas en el mismo programa

Fecha_inicio = "2022-07-01" # Fechas de inicio en caso de no seleccionar nada en la interfaz
Fecha_final = "2022-09-30"

print("Fecha Inicial Elegida: " + Fecha_inicio)
print("Fecha Final Elegida: " + Fecha_final)


colorppal = ['#440099', '#FF6A13', '#75787B'] # Colores principales
colorlist = ['#440099', '#AF97CC', '#FF6A13', '#66554B', '#75787B', '#8097AD']
colorfull = ['#440099', '#AF97CC', '#FF6A13', '#66554B', '#75787B', '#8097AD', '#6EB4FA', '#CC540E'] # Colores basados en paleta de colores de adobe

# DF para STN e Indicadores (en misma tabla de BD local)

prep_df(stndf) # Preparamos el DF de BD local
stndf = stndf.loc[(stndf["fecha"] <= Fecha_final )].reset_index()


stndf["Ingreso Neto Sin Contribuciones"] = stndf["ContribucionesSinC"].apply(format)
stndf["Ingreso Neto Con Contribuciones"] = stndf["ContribucionesConC"].apply(format)
stndf["FAER"] = stndf["FAER"].apply(format)
stndf["FOES"] = stndf["FOES"].apply(format)
stndf["PRONE"] = stndf["PRONE"].apply(format)
stndf["Demanda STN"] = stndf["Demanda_STN"].apply(format)

## DFs para Graficas
Grafica_ContribucionesDF = stndf.head(3).sort_values("fecha")[["Mes", "FOES", "PRONE", "FAER"]].set_index("Mes")
Grafica_IPPyIPC_DF = stndf.head(3).sort_values("fecha")[["Mes", "IPP", "IPC"]].set_index("Mes")
Grafica_IPPIyTCRM_DF = stndf.head(3).sort_values("fecha")[["Mes", "IPPI", "TCRM"]].set_index("Mes")
Grafica_CargosT_DF = stndf.head(3).sort_values("fecha")[["Mes", "T_Max", "T_Med", "T_Min", "T_Monomio"]].set_index("Mes")
Grafica_IngresosSTN_DF = stndf.head(3).sort_values("fecha")[["Mes","Ingreso Neto Sin Contribuciones", "Ingreso Neto Con Contribuciones"]].set_index("Mes")
Grafica_DemandaSTN_DF = stndf.head(3).sort_values("fecha")[["Mes","Demanda STN"]].set_index("Mes")
Grafica_IPP_IPCyIPPI_DF = stndf.head(3).sort_values("fecha")[["Mes", "IPP", "IPC", "IPPI"]].set_index("Mes")
Grafica_TCRM_DF = stndf.head(3).sort_values("fecha")[["Mes", "TCRM"]].set_index("Mes")

## DFs para analisis

Analisis_CargosT_DF = stndf.head(4).sort_values("fecha")[["Mes", "T_Max", "T_Med", "T_Min", "T_Monomio"]].set_index("Mes")
Analisis_Contribuciones_DF = stndf.head(4).sort_values("fecha")[["Mes", "FOES", "PRONE", "FAER"]].set_index("Mes")
Analisis_Ingresos_DF = stndf.head(4).sort_values("fecha")[["Mes","Ingreso Neto Sin Contribuciones", "Ingreso Neto Con Contribuciones"]].set_index("Mes")


## Grafica 1.1 = IPP e IPC
# print(Grafica_IPPyIPC_DF)
# title_font = {'fontname' : 'Helvetica'}

### --------------------- RECORDAR EJECUTAR PROCESADOR DE IMAGENES ---------------------
plt.style.use('seaborn-darkgrid')
ax1, ax2 = Grafica_IPPyIPC_DF.plot.line(subplots= True, marker = 'o', color = ['#440099', '#FF6A13'], linewidth = 2, fontsize = 13, figsize = (6,6))
plt.xlabel('Mes', fontsize = 14)
ajuste_dis_IPPeIPC = [-0.05,0.95,1.95]
for idx in range(len(Grafica_IPPyIPC_DF)):
    ax1.text(ajuste_dis_IPPeIPC[idx], Grafica_IPPyIPC_DF['IPP'][idx] - 0.15, round(Grafica_IPPyIPC_DF['IPP'][idx]), size = 12)
    ax2.text(ajuste_dis_IPPeIPC[idx], Grafica_IPPyIPC_DF['IPC'][idx] + 0.15, round(Grafica_IPPyIPC_DF['IPC'][idx]), size = 12)
# ax1.set_ylabel('Valor IPP', fontsize = 15)
# ax2.set_ylabel('Valor IPC', fontsize = 15)
ax1.set_title('IPP e IPC', fontsize = 15)
ax1.grid()
ax2.grid()
ax1.legend(fontsize = 13)
ax2.legend(fontsize = 13)
plt.xticks(fontsize = 14)
plt.xlabel(" ")
plt.savefig(r"Temp\{name}.png".format(name="IPPeIPC"), bbox_inches='tight')

trimestre = get_meses_trimestre(Grafica_IPPyIPC_DF)
año = get_año(stndf)

## Grafica 1.2 - IPPI y TCRM
ax1, ax2 = Grafica_IPPIyTCRM_DF.plot.line(subplots= True, marker = 'o', color = ['#440099', '#FF6A13'], linewidth = 2, fontsize = 13, figsize = (6,6))
plt.xlabel('Mes')
ajuste_dis_IPPIyTCRM = [-0.05,0.95,1.95]
for idx in range(len(Grafica_IPPIyTCRM_DF)):
    ax1.text(ajuste_dis_IPPIyTCRM[idx], Grafica_IPPIyTCRM_DF['IPPI'][idx] - 0.075, round(Grafica_IPPIyTCRM_DF['IPPI'][idx]), size = 12)
    ax2.text(ajuste_dis_IPPIyTCRM[idx], Grafica_IPPIyTCRM_DF['TCRM'][idx] + 5, round(Grafica_IPPIyTCRM_DF['TCRM'][idx]), size = 12)
# ax1.set_ylabel('Valor IPP Industria', fontsize = 14)
# ax2.set_ylabel('Valor TCRM', fontsize = 14)
ax1.set_title('IPP Industria y TCRM', fontsize = 14)
ax1.grid()
ax2.grid()
ax1.legend(fontsize = 13)
ax2.legend(fontsize = 13)
plt.xticks(fontsize = 14)
plt.xlabel(" ")
plt.savefig(r"Temp\{name}.png".format(name="IPPIyTCRM"), bbox_inches='tight')

## Graficas alternativas de Indicadores
# Los IP´s

# ax = Grafica_IPP_IPCyIPPI_DF.plot.line(marker = 'o', color = ['#440099', '#FF6A13', '#75787B'], linewidth = 2)
# plt.xlabel('Mes')
# ajuste_dis_IPP_IPC_yIPPI = [-0.05,0.95,1.95]
# for idx in range(len(Grafica_IPP_IPCyIPPI_DF)):
#     ax.text(ajuste_dis_IPP_IPC_yIPPI[idx], Grafica_IPP_IPCyIPPI_DF['IPP'][idx] - 3.5, round(Grafica_IPP_IPCyIPPI_DF['IPP'][idx]), size = 12)
#     ax.text(ajuste_dis_IPP_IPC_yIPPI[idx], Grafica_IPP_IPCyIPPI_DF['IPC'][idx] + 1, round(Grafica_IPP_IPCyIPPI_DF['IPC'][idx]), size = 12)
#     ax.text(ajuste_dis_IPP_IPC_yIPPI[idx], Grafica_IPP_IPCyIPPI_DF['IPPI'][idx] - 3.5, round(Grafica_IPP_IPCyIPPI_DF['IPPI'][idx]), size = 12)
# ax.set_title('Indicadores', fontsize = 14)
# ax.grid()

# plt.savefig(r"Temp\{name}.png".format(name="Indicadores_alt"))

# # TCRM
# ax = Grafica_TCRM_DF.plot.line(marker = 'o', color = '#440099', linewidth = 2)
# plt.xlabel('Mes')
# ajuste_dis_TCRM = [-0.05,0.95,1.95]
# for idx in range(len(Grafica_IPPIyTCRM_DF)):
#     ax.text(ajuste_dis_TCRM[idx], Grafica_TCRM_DF['TCRM'][idx] + 5, round(Grafica_TCRM_DF['TCRM'][idx]), size = 12)
# ax.set_title('Indicador TCRM', fontsize = 14)
# ax.grid()
# plt.savefig(r"Temp\{name}.png".format(name="TCRM_alt"))

## STN

## Grafica 2 - Cargos T
ax = Grafica_CargosT_DF.plot.line(marker = 'o', color = ['#440099', '#FF6A13', '#2AD2C9','#00966C'], linewidth = 2, figsize = (6,5))
ajuste_dis = [-0.05,0.95,1.95]
for idx in range(len(Grafica_CargosT_DF)):
    ax.text(ajuste_dis[idx], Grafica_CargosT_DF['T_Max'][idx] - 0.8, round(Grafica_CargosT_DF['T_Max'][idx],1), size = 10)
    ax.text(ajuste_dis[idx], Grafica_CargosT_DF['T_Min'][idx] + 0.3, round(Grafica_CargosT_DF['T_Min'][idx],1), size = 10)
    ax.text(ajuste_dis[idx], Grafica_CargosT_DF['T_Monomio'][idx] + 0.5, round(Grafica_CargosT_DF['T_Monomio'][idx],1), size = 10)
plt.xlabel('Mes')
plt.ylabel('Cargos T')
plt.title('Cargos T (COP/kWh)')
plt.grid()
plt.savefig(r"Temp\{name}.png".format(name="STN_Cargos_T"))

## Grafica 3 - Ingresos sin y con contribuciones
realizar_grafica(Grafica_IngresosSTN_DF, "STN_Ingresos", 'Ingresos STN (COP)', tipoG = 'Ingresos STN') # Invocar funciones de arriba

## Grafica 4 - Contribuciones
realizar_grafica(Grafica_ContribucionesDF, "STN_Contribuciones", 'Contribuciones (COP)', tipoG = 'Contribuciones')

## Grafica 5 - Demanda STN
realizar_grafica(Grafica_DemandaSTN_DF, "STN_Demanda", "Demanda STN (kWh)", tipoG = 'Demanda STN')


## Graficas del STR
# (nada que no se halla hecho en el STN)
prep_df(strdf)
strdf = strdf.loc[(strdf["fecha"] <= Fecha_final )].reset_index()

strdf["Ing STR Norte"] = strdf["IngSTR1"].apply(format)
strdf["Ing STR Centro Sur"] = strdf["IngSTR2"].apply(format)
strdf["Demanda STR Norte"] = strdf["DemandaSTR1"].apply(format)
strdf["Demanda STR Centro Sur"] = strdf["DemandaSTR2"].apply(format)


## Grafica 5 - Ingresos OR STRs

Grafica_IngSTR_DF = strdf.head(3).sort_values("fecha")[["Mes", "Ing STR Norte","Ing STR Centro Sur"]].set_index("Mes")
realizar_grafica(Grafica_IngSTR_DF, "STR_Ingresos", 'Ingresos en los Operadores de Red (COP)', tipoG = 'Ingresos STR') 

mesesSTR = Grafica_IngSTR_DF.head(3).index.tolist()

# Get mes max de ingSTR (MM)
max_ing_STR = Grafica_IngSTR_DF.max().max()
MM_Ing_STR = Grafica_IngSTR_DF[Grafica_IngSTR_DF['Ing STR Centro Sur']==max_ing_STR].index.values[0]


## Grafica 6 - Cargos del STR

strdf["CD4 STR Norte"] = strdf["CD4STR1"]
strdf["CD4 STR Centro Sur"] = strdf["CD4STR2"]
strdf["DT4 STR Norte"] = strdf["DT4STR1"]
strdf["DT4 STR Centro Sur"] = strdf["DT4STR2"]

Grafica_CargosSTR_DF = strdf.head(3).sort_values("fecha")[["Mes", "CD4 STR Norte", "CD4 STR Centro Sur", "DT4 STR Norte", "DT4 STR Centro Sur"]].set_index("Mes")
ax = Grafica_CargosSTR_DF.plot.line(marker = 'o', color = ['#440099', '#FF6A13', '#75787B','#00966C'], linewidth = 2, figsize = (6,5))
for idx in range(len(Grafica_CargosSTR_DF)):
    ax.text(ajuste_dis[idx], Grafica_CargosSTR_DF["CD4 STR Norte"][idx] - 0.8, round(Grafica_CargosSTR_DF["CD4 STR Norte"][idx],1), size = 10)
    ax.text(ajuste_dis[idx], Grafica_CargosSTR_DF["CD4 STR Centro Sur"][idx] - 0.8, round(Grafica_CargosSTR_DF["CD4 STR Centro Sur"][idx],1), size = 10)
    ax.text(ajuste_dis[idx], Grafica_CargosSTR_DF["DT4 STR Norte"][idx] + 0.5, round(Grafica_CargosSTR_DF["DT4 STR Norte"][idx],1), size = 10)
    ax.text(ajuste_dis[idx], Grafica_CargosSTR_DF["DT4 STR Centro Sur"][idx] + 0.5, round(Grafica_CargosSTR_DF["DT4 STR Centro Sur"][idx],1), size = 10)
plt.xlabel('Mes')
plt.title('Cargos STR (COP/kWh)')
plt.grid()
plt.savefig(r"Temp\{name}.png".format(name="STR_Cargos"))

max_DT4 = Grafica_CargosSTR_DF.max().max()
MM_Cargos = Grafica_CargosSTR_DF[Grafica_CargosSTR_DF['DT4 STR Norte']==max_DT4].index.values[0]


## Grafica 7 - Demanda del STR

Grafica_DemandaSTR_DF = strdf.head(3).sort_values("fecha")[["Mes", "Demanda STR Norte","Demanda STR Centro Sur"]].set_index("Mes")
realizar_grafica(Grafica_DemandaSTR_DF, "STR_Demanda", 'Demanda Energetica en el STR (kWh)', tipoG = 'Demanda STR') 

# Get mes max de DemandaSTR (MM)
max_Demanda_STR = Grafica_DemandaSTR_DF.max().max()
MM_Demanda_STR = Grafica_DemandaSTR_DF[Grafica_DemandaSTR_DF['Demanda STR Centro Sur']==max_Demanda_STR ].index.values[0]


## Graficas ADDs
# Para ADDs hay un problema y es que se tienen que buscar registros de dos meses para atras.
# Esto dado que las publicaciones de las liquidaciones atrasadas m-2.

Fecha_inicio_d = datetime.strptime(Fecha_inicio, '%Y-%m-%d') # Se cambia a formato datetime las fechas escogidas en intefaz
Fecha_final_d = datetime.strptime(Fecha_final, '%Y-%m-%d')

fecha_adds_m2_Ini = add_months(Fecha_inicio_d, -2) # Se restan dos meses a las fechas nuevas para la consulta
fecha_adds_m2_Fin = add_months(Fecha_final_d, -2)

prep_df(addsdf)
addsdf = addsdf.loc[(addsdf["fecha"] <= Fecha_final )].reset_index().drop(columns = ["index"]) # Igual se deja el DF hasta el tope de ser necesarias las nuevas fechas

addsdf["NT"] = addsdf["NivelTension"]
addsdf["Ingreso Real"] = addsdf["IngR"].apply(format)
addsdf["Ingreso por ADD"] = addsdf["IngADD"].apply(format)

# Funcion Graficas ADDs
# Para realizar las graficas de ADDs se usa la antigua funcion de realizar_grafica del STN y STR pero con modificaciones
def realizar_grafica_ADD(Area, ImgName, titleADD):
    add1 = (addsdf[(addsdf["fecha"] >= fecha_adds_m2_Ini) & (addsdf["fecha"] <= fecha_adds_m2_Fin)]) # filtrado y organizado por fecha
    add1 = add1[add1['Area'] == Area ].sort_values(by='fecha', ascending = False).head(9) # Top 9 entradas de dicha fecha (por si aparece otro registro que no pertenece (nada raro en cargosADD))
    add_DF1 = add1.sort_values("fecha")[["Mes", "NT", "Ingreso Real", "Ingreso por ADD"]].set_index('Mes')
    MesesADD = add_DF1.index.tolist() # Necesario para doc de exporte
    AñosADD = add1["Año"].tolist()
    add_DF = pd.pivot_table(add_DF1, values = ['Ingreso Real','Ingreso por ADD'], index = ['Mes', 'NT']) # Pivoteamos la tabla para obtener los datos en orden
    realizar_grafica(add_DF, ImgName, titleADD, (6,4)) 
    xticks = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    xticks_lab = ['NT1', 'NT2 \n' + MesesADD[2],
                'NT3','NT1', 'NT2 \n' + MesesADD[5],
                'NT3','NT1', 'NT2 \n' + MesesADD[8], 'NT3']

    # La grafica tiene doble indicie en el eje x, para mostrar los ingresos de los 3 NT

    plt.xticks(xticks, xticks_lab)
    plt.xlabel(" ")

    save = plt.savefig(r"Temp\{name}.png".format(name=ImgName))
    return save, MesesADD, AñosADD

realizar_grafica_ADD('ADD Oriente', 'ADD_Oriente', 'Ingresos a OR de ADD Oriente (COP)') # Invocar funciones
realizar_grafica_ADD('ADD Occidente', 'ADD_Occidente', 'Ingresos a OR de ADD Occidente (COP)')
realizar_grafica_ADD('ADD Centro', 'ADD_Centro', 'Ingresos a OR de ADD Centro (COP)')
realizar_grafica_ADD('ADD Sur', 'ADD_Sur', 'Ingresos a OR de ADD Sur (COP)')
# Area es el parametro por el cual se filtra en la columna de del ADD asociado
# ImgName es como se nombra la grafica y tittleADD es el titulo que se le pone a la grafica

a, MesesADD, AñosADD = realizar_grafica_ADD('ADD Centro', 'ADD_Centro', 'Ingresos a OR de ADD Centro (COP)') # Valores necesarios para el doc de exporte


## Conovcatorias STN y SDL
# En convocatorias se buscan las anualidades que empiezan para el periodo seleccionado
# CUIDADO! si se selecciona la fecha inicial o final en el dia equivocado es altamente probable que no reguistre varias convocatorias

convdf["FechaInicial"] = pd.to_datetime(convdf["FechaInicial"]) # Cambiar toda la columna de conv de fechas a datetimes
convdf["FechaFinal"] = pd.to_datetime(convdf["FechaFinal"]) # x2

FechaFin_conv = Fecha_final
FechaIni_conv = Fecha_inicio

ConvQueInician_DF = convdf.loc[(convdf["FechaInicial"] >= FechaIni_conv ) & (convdf["FechaInicial"] <= FechaFin_conv )].reset_index() # Fitrar el DF de la BD local para esas fechas seleccionadas

ConvQueInician_DF["MesIni"]= ConvQueInician_DF["FechaInicial"].dt.month_name(locale='Spanish')
ConvQueInician_DF["AñoIni"]= ConvQueInician_DF["FechaInicial"].dt.year


ConvList = []

for i in range(len(ConvQueInician_DF)): # Si la convocatoria es del STR o del STN
    if "STR" in ConvQueInician_DF.at[i,"Nombre"]:
        ConvString = 'En el STR a partir de ' + ConvQueInician_DF.at[i,"MesIni"].lower() + ' del ' + str(ConvQueInician_DF.at[i,"AñoIni"]) + ', se inició la anualidad número '   + ConvQueInician_DF.at[i,"NAnualidad"]  + ' utilizada para calcular la remuneración del proyecto '  + ConvQueInician_DF.at[i,"Nombre"]  + " (" + ConvQueInician_DF.at[i,"Descripcion"] + ")" + ' conforme a lo establecido en la ' + ConvQueInician_DF.at[i,"Resolucion"]
    else:
        ConvString = 'En el STN a partir de ' + ConvQueInician_DF.at[i,"MesIni"].lower() + ' del ' + str(ConvQueInician_DF.at[i,"AñoIni"]) + ', se inició la anualidad número '   + ConvQueInician_DF.at[i,"NAnualidad"]  + ' utilizada para calcular la remuneración del proyecto '  + ConvQueInician_DF.at[i,"Nombre"]  + " (" + ConvQueInician_DF.at[i,"Descripcion"] + ")" + ' conforme a lo establecido en la ' + ConvQueInician_DF.at[i,"Resolucion"]
    ConvList.append(ConvString) # ConvList es la lista de cada string de convocatorias que va en el documento de exporte  (se elimina el valor en USD o COP)

## Graficas SDL

sdldf["fecha"] = pd.to_datetime(sdldf["fecha"]) # Nada nuevo
sdldf["fecha"] = sdldf.progress_apply(lambda row: add_months(row["fecha"], 2), axis = 1) 
# El Query esta tomado desde CargosADD, que da los cargos 2 meses atrasados para darlos con la liquidacion, pero en realidad son 2 meses adelante
# Si no me crees, que es normal, yo tampoco lo haría, puedes revisar el query de Carper para verificar que las fechas con los cargos ahí esten bien

prep_df(sdldf)

Areas_MercadoDF = (sdldf[(sdldf["NT"] == "1") & (sdldf["fecha"] == Fecha_inicio)])[["Area", "Mercado"]] # Solamente se grafica el DT1 y el DTUN en caso ser ADD

prep_df(sdldfsinADD) # Este es el DF de los OR sin ADD, como no tienen DTUN, el DF debe ser diferente
sdldfsinADD= (sdldfsinADD[(sdldfsinADD["fecha"] >= Fecha_inicio) & (sdldfsinADD["fecha"] <= Fecha_final)])
sdldfsinADD = sdldfsinADD.merge(Areas_MercadoDF, on = "Mercado", how = "outer")[["fecha", "Mercado", "Tipo", "Comercializador", "DT1", "Mes", "Año"]].reset_index()

fecha_entrada_tolima = datetime.strptime('2023-07-01', '%Y-%m-%d')

def realizar_grafica_SDL(GraficaDF, AreaName = 'ADD Centro', ImgName = "No name", title = "No Title", nORs = 7): # Necesitamos el numero de ORs para los lab y numero de graficas
    # Si algun dia hay OR nuevo se puede modificar desde aqui
    if AreaName == "NaN": 
        df1 = (GraficaDF[(GraficaDF["fecha"] >= Fecha_inicio) & (GraficaDF["fecha"] <= Fecha_final)])
        df1 = (GraficaDF[(GraficaDF["Comercializador"] == "None") & (GraficaDF["Tipo"] == "6")]).sort_values(["fecha", "Mercado"]).reset_index()[["fecha", "Mes", "Mercado", "Tipo", "DT1"]].reset_index()
        if Fecha_inicio_d < fecha_entrada_tolima:
            df_dtun = df1.filter(items = [0,4,9], axis = 0)
            nORs = 5
        ListMerc = df1["Mercado"].head(nORs).tolist() # Se crea lista de los mercados fuera de ADD
        df11 = df1[df1["Mercado"] == ListMerc[0]] # Se grafica para el primer mercado la linea y se crea el eje ax
        ax = df11.plot.line(x = "Mes", y = "DT1", label = ListMerc[0], color = colorfull[0], marker = '.', figsize = (6,4))
        for i in range(nORs - 1):
            dfi = df1[df1["Mercado"] == ListMerc[i+1]]
            dfi.plot(x = "Mes", y = "DT1", ax=ax, label = ListMerc[i+1], color = colorfull[i+1], marker = '.', figsize = (6,4))
            # Se grafica las otras lineas para los otros mercados
        # xticks = [1,5.5,9.5]

    else:
        df1 = (GraficaDF[(GraficaDF["Area"] == AreaName) & (GraficaDF["fecha"] >= Fecha_inicio) & (GraficaDF["fecha"] <= Fecha_final)]).sort_values(["fecha", "Mercado"])[["fecha", "Mes", "Mercado", "DT", "DtUN", "NT"]]
        df1 = df1[df1["NT"] == '1'].reset_index()[["Mes", "Mercado", "DT", "DtUN"]].reset_index()

        # Acá tenemos un problema para eliminar los duplicados de DtUN, dado que si se tiene el mismo DTUN para una ADD en diferentes meses se van a eliminar
        # Ejemplo: Para ADD oriente en Nov-2022 tenemos duplicados entonces la grafica queda coja entonces toca crear una anomalia pa esto
        # No solo eso, sino que ademas Tolima entra en Julio - 2022, haciendo mas dificil la lectura de DT - DTUN

        if AreaName == 'ADD Oriente':
            df_dtun = df1.filter(items = [0,5,10], axis = 0)
            nORs = 5
            if Fecha_final_d < fecha_entrada_tolima:
                df_dtun = df1.filter(items = [0,4,9], axis = 0)
                nORs = 4
        else:
            df_dtun = df1.drop_duplicates(subset = ["DtUN"])

        ListMerc = df1["Mercado"].head(nORs).tolist()
        df1[df1["Mercado"] == ListMerc[0]]
        ax = df_dtun.plot(x='Mes', y='DtUN', label = "DtUN " + AreaName, linewidth = 3, figsize = (6,4), color = colorfull[0])
        # Primero graficamos el DTUn para cada ADD, definiendo el eje ax
        for i in range (nORs): # Luego graficamos cada una de las lineas consecuentes con el DT de cada mercado
            dfi = df1[df1["Mercado"] == ListMerc[i]]
            dfi.plot(x = "Mes", y = "DT", kind = "line", ax=ax, label = ListMerc[i], color = colorfull[i+1], marker = '.', figsize = (6,4))
        # xticks = [3,10,17]

    # if AreaName == "ADD Sur":
    #     xticks = [0.5,8.5,15.5]
    # elif AreaName == "ADD Oriente":
    #     xticks = [1,7,13]

    # xticks_lab = [mesesSTR[0], mesesSTR[1], mesesSTR[2]]
    # plt.xticks(xticks, xticks_lab)
    plt.legend(loc='lower center', bbox_to_anchor=(0.25, -0.6)) # Esto es para sacar los lab de la imagen, ya que sino pueden pisar las lineas
    # plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='upper left', mode="expand", borderaxespad=0.)
    plt.title(title)
    plt.xlabel("Mes")
    plt.title(title)
    save = plt.savefig(r"Temp\{name}.png".format(name=ImgName), bbox_inches='tight')
    return save

realizar_grafica_SDL(sdldf, "ADD Centro",  "SDL_Cargos_Centro", 'Cargo DT1 y DTUN para ORs de ADD Centro (COP/kWh)',7)
realizar_grafica_SDL(sdldf, "ADD Occidente", "SDL_Cargos_Occidente", 'Cargo DT1 y DTUN para ORs de ADD Occidente (COP/kWh)',7)
realizar_grafica_SDL(sdldf, "ADD Oriente", "SDL_Cargos_Oriente", 'Cargo DT1 y DTUN para ORs de ADD Oriente (COP/kWh)',5)
realizar_grafica_SDL(sdldf, "ADD Sur", "SDL_Cargos_Sur", 'Cargo DT1 y DTUN para ORs de ADD Sur (COP/kWh)',6)
realizar_grafica_SDL(sdldfsinADD, "NaN", "SDL_Cargos_sinADD", 'Cargo DT1 para ORs sin ADD (COP/kWh)',4)
# GraficaDF es el DF que se usa para graficar, Area es el nombre de la ADD a filtrar
# ImgName y tittle son iguales que ADDs y nORs es el modificable para numero de ORs dentro de ADD


## CPROG
# Basicamente lo mismo que el SDL pero mas sencillo
prep_df(cprogdf)

cprogdf_add = cprogdf.merge(Areas_MercadoDF, on = "Mercado", how = "outer")[["fecha", "Mercado", "Area", "CPROG", "Mes", "Año"]]
cprogdf2 = (cprogdf_add[(cprogdf_add["fecha"] >= Fecha_inicio) & (cprogdf_add["fecha"] <= Fecha_final)]).sort_values(by = ["fecha", "Mercado"])

def realizar_grafica_CPROG(GraficaDF, AreaName, ImgName, title, nORs):
    if AreaName == 'NaN':
        df1 = GraficaDF[GraficaDF["Area"].isnull()][["Mes", "Mercado", "CPROG"]]
    else:
        df1 = GraficaDF[GraficaDF["Area"] == AreaName][["Mes", "Mercado", "CPROG"]]
    ListMerc = df1["Mercado"].head(nORs).tolist()

    df11 = df1[df1["Mercado"] == ListMerc[0]]
    ax = df11.plot(x='Mes', y='CPROG', label = ListMerc[0], color = colorfull[0], marker = '.', figsize = (6.5,4))
    for i in range (nORs - 1):
        dfi = df1[df1["Mercado"] == ListMerc[i+1]]
        dfi.plot(x = "Mes", y = "CPROG", ax=ax, label = ListMerc[i+1], color = colorfull[i+1], marker = '.', figsize = (6.5,4))

    plt.legend(loc='lower center', bbox_to_anchor=(0.25, -0.6))
    # plt.xlim(-0.1, 5) 
    plt.title(title)
    save = plt.savefig(r"Temp\{name}.png".format(name=ImgName), bbox_inches='tight')
    return save

realizar_grafica_CPROG(cprogdf2, 'ADD Centro', 'CPROG_Centro', 'Cargo CPROG para ADD Centro (COP/kWh)', 7)
realizar_grafica_CPROG(cprogdf2, 'ADD Oriente', 'CPROG_Oriente', 'Cargo CPROG para ADD Oriente (COP/kWh)', 5)
realizar_grafica_CPROG(cprogdf2, 'ADD Occidente', 'CPROG_Occidente', 'Cargo CPROG para ADD Occidente (COP/kWh)', 7)
realizar_grafica_CPROG(cprogdf2, 'ADD Sur', 'CPROG_Sur', 'Cargo CPROG para ADD Sur (COP/kWh)', 6)
realizar_grafica_CPROG(cprogdf2, 'NaN', 'CPROG_sinADD', 'Cargo CPROG para OR sin ADD (COP/kWh)',4)

## Calidad SDL
# Los indicadores de Calidad se dan por mercado y se pueden separar tambien por grupos de ADD, pero el informe ya va por 20pgs
# Es lo mismo que la funcion de realizar_grafica pero con la facilidad de que no hay numeros muy grandes
prep_df(calidaddf)

caldf = (calidaddf[(calidaddf["fecha"] >= Fecha_inicio) & (calidaddf["fecha"] <= Fecha_final)]).sort_values("fecha")[["SAIDI", "SAIFI", "Mes"]].set_index("Mes")
ax = caldf.plot.bar(rot = 0, color = ['#440099', '#FF6A13', '#75787B'], figsize = (5,5))
ajuste_dis_1 = [-0.2,0.8,1.8]
ajuste_dis_2 = [0.05,1.05,2.05]
for idx in range(len(caldf)):
    ax.text(ajuste_dis_1[idx], caldf["SAIDI"][idx] + 0.05, round(caldf["SAIDI"][idx],1), size = 9)
    ax.text(ajuste_dis_2[idx], caldf["SAIFI"][idx] + 0.05, round(caldf["SAIFI"][idx],1), size = 9)
plt.title("Indicadores de calidad en SDL a nivel pais")
save = plt.savefig(r"Temp\{name}.png".format(name="Calidad_SDL"))



## Analisis en STN (FOES b)}
# Para realizar los strings de analisis en los procesos de STN y STR requerimos hacer comparaciones de sus valores

contString = []
ingSTNString = []
cargosTString = []

# Analisis Contribuciones
for i in range(len(Analisis_Contribuciones_DF) - 1): # Se toma el DF de grafica y se le incluye el registro anterior al primero graficado 
    if Analisis_Contribuciones_DF['FOES'][i + 1] > Analisis_Contribuciones_DF["FOES"][i]: # se comparan estos registros para diferentes variables
        contString.append(' las contribuciones en el STN aumentaron principalemtne debido a ') # si se tiene una diferencia positiva se añade un string
    else:
        contString.append(' las contribuciones en el STN disminuyeron principalemtne debido a ') # si se tiene una diferencia negativa se añade otro 

# Analisis Ingresos STN
for i in range(len(Analisis_Ingresos_DF) - 1):
    if Analisis_Ingresos_DF['Ingreso Neto Sin Contribuciones'][i + 1] > Analisis_Ingresos_DF["Ingreso Neto Sin Contribuciones"][i]:
        ingSTNString.append(' los ingresos en el STN aumentaron principalemtne debido a ')
    else:
        ingSTNString.append(' los ingresos en el STN disminuyeron principalemtne debido a ')

# Analisis Cargos T
for i in range(len(Analisis_CargosT_DF) - 1):
    if Analisis_CargosT_DF['T_Monomio'][i + 1] > Analisis_CargosT_DF['T_Monomio'][i]:
        cargosTString.append(' los cargos en el STN aumentaron principalemtne debido a ')
    else:
        cargosTString.append(' los cargos en el STN disminuyeron principalemtne debido a ')   


print("Done Main!")




