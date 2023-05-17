import numpy as np
import pandas as pd
import sqlite3
from Connections import (IPP_y_TCRMDF, IPPI_DF, IPC_DF, ContribucionesDF, Cargos_STNDF, Balance_cargosDF, addsDF, str1DF, str2DF)

# Proceso STN
STNbigDF = IPP_y_TCRMDF.merge(ContribucionesDF,on="FECHA").merge(Balance_cargosDF,on="FECHA").merge(IPPI_DF, on= "FECHA").merge(IPC_DF, on= "FECHA").merge(Cargos_STNDF, left_on= "FECHA", right_on = "FECHINIC")
STNbigDF["CONTRIBUCIONES1"] = abs(STNbigDF["TRANSMISORES"])
STNbigDF["CONTRIBUCIONES2"] = STNbigDF["CONTRIBUCIONES1"] - STNbigDF["FAER"] - STNbigDF["FOES"] - STNbigDF["PRONE"]
STNDF = STNbigDF[["FECHA","CONTRIBUCIONES1","FAER","FOES","PRONE","CONTRIBUCIONES2", "IPP", "IPC", "IPPI", "TCRM", "T_NETO_MAXIMA", "T_NETO_MEDIA", "T_NETO_MINIMA", "T_NETO_MONOMIO"]]

# Proceso ADDs
ADDDF = addsDF[["Fecha", "NT","ADD","IngR","IngADD"]]

# Proceso STR
STRDF = str1DF.merge(str2DF, on = "fechaTrabajo")

finalconn = sqlite3.connect('variablesDB.db')
finalCursor = finalconn.cursor()

for row in STNDF.itertuples():
    insert_sql_STN = f"INSERT INTO variablesSTN (fecha, ContribucionesConC, FAER, FOES, PRONE, ContribucionesSinC, IPP, IPC, IPPI, TCRM, T_Max, T_Med, T_Min, T_Monomio) VALUES ('{row[1]}', {row[2]}, {row[3]}, {row[4]}, {row[5]}, {row[6]}, {row[7]}, {row[8]}, {row[9]}, {row[10]}, {row[11]}, {row[12]}, {row[13]}, {row[14]})"
    finalCursor.execute(insert_sql_STN)

for row in ADDDF.itertuples():
    insert_sql_ADDs = f"INSERT INTO variablesADDs (fecha, NivelTension, Area, IngR, IngADD) VALUES ('{row[1]}', '{row[2]}', '{row[3]}', {row[4]}, {row[5]})"
    finalCursor.execute(insert_sql_ADDs)

for row in STRDF.itertuples():
    insert_sql_STR = f"INSERT INTO variablesSTR (fecha, IngSTR1, IngSTR2) VALUES ('{row[1]}', {row[2]}, {row[3]})"
    finalCursor.execute(insert_sql_STR)

finalconn.commit()

print('Done ConstructorSQLite!')