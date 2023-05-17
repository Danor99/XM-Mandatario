from datetime import datetime, timedelta, date
import pandas as pd
from ConsultaBD import ConexionOra
from typing import List


def getOracleConnection(user:str, password:str):
    try:
        con=ConexionOra(user=user, password=password, database='ORASICP.XM')
        print('Conection sucessfull in SQL server')
        return con
    except:
        return None

def readSQLFile(filename:str):
    filename='Queries\\'+filename
    with open(filename,'r') as F:
        query=F.read()
    return query

def getIPP(dateList:List[datetime], cnx, filename='IPP.sql'):
    mod=["TO_DATE('{}','YYYYMMDD')".format(datum.strftime('%Y%m%d')) for datum in dateList]
    mod=','.join(mod)
    query=readSQLFile(filename=filename)
    query=query.replace("TO_DATE('20201001','YYYYMMDD')",mod)

    df=cnx.consultar(query)
    return df

def getIPC(dateList:List[datetime], cnx, filename='IPC.sql'):
    mod=["TO_DATE('{}','YYYYMMDD')".format(datum.strftime('%Y%m%d')) for datum in dateList]
    mod=','.join(mod)
    query=readSQLFile(filename=filename)
    query=query.replace("TO_DATE('20201001','YYYYMMDD')",mod)

    df=cnx.consultar(query)
    return df

def getIPPInd(dateList, cnx): #BUscar la series industria en BBDD esta en oracle
    mod=["TO_DATE('{}','YYYYMMDD')".format(datum.strftime('%Y%m%d')) for datum in dateList]
    query=f"SELECT A302FECHA FECHA, A302VALOR IPP FROM T302VALORESINDICADORES WHERE A302IDINDICADOR = 95 AND A302CONSECUTIVO = 1 AND A302FECHA IN ({','.join(mod)}) ORDER BY FECHA DESC"
    df=cnx.consultar(query)
    return df

def mergeIPP(df, dfIPP, columnName, columnImputer):
    for _, row in dfIPP.iterrows():
        date, value= row
        df.loc[df[columnName]==date,columnImputer]=value
    return df

def get027Varibles(period):
    df = pd.read_excel('Cargos CPROG_V3.xlsx', sheet_name = 'FechaIniVig', nrows= 50, usecols = 'A,L:M') 
    df.columns = ['Market', 'isin027','MonthBase']
    df = df.loc[df['isin027'] == True] 
    df['MonthBase']=pd.to_datetime(df['MonthBase'])
    return df[['Market','MonthBase']].copy()

def get027Index(period, user, password):
    dbORA=getOracleConnection(user=user, password=password)
    df027=get027Varibles(period) ## Esta debe traer el mercado y la fecha de referencia 
    if df027.shape[0]!=0:
        dates=[x.replace(day=1) for x in df027.MonthBase]
        dates.append(datetime(2017,12,1))
        dates.append(datetime(2007,12,1))
        dates.append(datetime(2022,9,1))
        period_m1=period+timedelta(days=-1)
        period_m1=period_m1.replace(day=1)
        period_m1=period_m1+timedelta(days=-1)
        period_m1=period_m1.replace(day=1)
        dates.append(period_m1)
        dfIPP027=getIPP(dates, dbORA)
        dfIPC027=getIPC(dates, dbORA)
        dfIPPIndustria=getIPPInd(dates, dbORA)

        df027=mergeIPP(df027,dfIPP027,'MonthBase','IPPref')
        df027=mergeIPP(df027,dfIPC027,'MonthBase','IPCref')
        dfInd=dfIPPIndustria.copy()
        dfInd.columns=['MonthBase', 'IPPref*']
        df027=df027.merge(dfInd, on='MonthBase')
        df027['IPP0']=dfIPP027[dfIPP027['FECHA']==datetime(2017,12,1)].IPP.values[0]
        df027['IPP_cv*']=dfIPPIndustria[dfIPPIndustria['FECHA']==datetime(2022,9,1)].IPP.values[0]
        df027['IPP_m*']=dfIPPIndustria[dfIPPIndustria['FECHA']==datetime.combine(period_m1, datetime.min.time())].IPP.values[0]
        df027['IPC_cv']=dfIPC027[dfIPC027['FECHA']==datetime(2022,9,1)].IPC.values[0]
        df027['IPC_m']=dfIPC027[dfIPC027['FECHA']==datetime.combine(period_m1, datetime.min.time())].IPC.values[0]
        df027['FactorReducCargo']=df027.apply(lambda x: min(x['IPP_m*']/x['IPP_cv*'],x['IPC_m']/x['IPC_cv']), axis=1)
        df027['Indexador027']=df027.apply(lambda x: (x['IPPref']/x['IPP0'])*(x['IPC_cv']/x['IPCref']), axis=1)
        df027['Factor']=df027['FactorReducCargo']*df027['Indexador027']
        df027['Factor']=df027['Factor'].apply(lambda x: round(x,9))

    return df027

if __name__=='__main__':
   df=get027Index(date(2023,4,1),'DOROZCO','Xerneas990!') 
   print(df)


