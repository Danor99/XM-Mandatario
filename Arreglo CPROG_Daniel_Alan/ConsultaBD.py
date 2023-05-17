# -*- coding: utf-8 -*-

import os
import pyodbc
import pandas as pd
import cx_Oracle
import sqlite3
from abc import ABC, abstractmethod


class Conexion(ABC):
    @abstractmethod
    def consultar(self):
        pass
    
    def getQuery(self, path:str, params:dict={}):
        with open(path, 'r') as SQL:
            SQL_string=SQL.read()
            SQL_string=SQL_string.format(**params) if len(params.keys())!=0 else SQL_string
        return SQL_string
    
    def consultaParams(self, path:str, params):
        query=self.getQuery(path, params)
        df=self.consultar(query)
        return df

class ConexionOra(Conexion):
    def __init__(self, user, password, database):
        self.user = user
        self.password = password
        self.database = database
        self.status = False
    
    def consultar(self, query:str, params=None):
        with cx_Oracle.connect(self.user, self.password, self.database) as connection:
            cursor = connection.cursor()
            if params == None:
                cursor.execute(query)
            else:
                cursor.execute(query, params)
            cursor.rowcount
            fields = [x[0] for x in cursor.description]    
            lista=cursor.fetchall()
            df = pd.DataFrame.from_records(lista, columns=fields)
        return df


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

class Publicacion(object):
    def __init__(self, name, rootDir, middleDir):
        self.name = name
        self.rootDir = rootDir
        self.middleDir = middleDir

    def getRecurso(self):
        None
    
    def getFolders(self, fecha, ext):
        filename=self.name+"{0:02d}{1:02d}".format(fecha.month,fecha.day)+'.'+ext      
        endString=os.path.join(self.middleDir, "{0}-{1:02d}".format(fecha.year,fecha.month),filename)
        files=[]
        directories = [f.path for f in os.scandir(self.rootDir) if f.is_dir()]
        for directory in directories:
            if os.path.exists(os.path.join(directory,endString)):
                files.append(os.path.join(directory,endString))
        return files
        

    def getData(self, fecha, ext):
        files = self.getFolders(fecha, ext)
        filesdf=[]
        for f in files:
            temp=pd.read_csv(f, delimiter=';')
            temp['path']=f
            filesdf.append(temp)
        df=pd.concat(filesdf)
        return df

class ConexionSQLite(Conexion):
    def __init__(self, path):
        self.path=path

    def consultar(self, query:str, params=None):
        try:
            conn=sqlite3.connect(self.path)
            cursor=conn.cursor()
            cursor.execute(query)
            rows=cursor.fetchall()
            names=[x[0] for x in cursor.description]
            result=pd.DataFrame(rows, columns=names)
            conn.close()
            return result
        except:
            print('La base de datos no esta disponible')
    
    def insert(self, query:str, data:list):
        conn=sqlite3.connect(self.path)
        cursor=conn.cursor()
        cursor.executemany(query, data)

    def insertDependiente(self, query1:str, query2:str, data1, data2):
        conn=sqlite3.connect(self.path)
        cursor=conn.cursor()
        cursor.execute(query1, data1)
        id=cursor.lastrowid
        for row in data2:
            cursor.execute(query2, [id, *row])
        conn.commit()
        conn.close()

if __name__=="__main__":
    pass