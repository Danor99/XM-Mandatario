import os
import pandas as pd
import numpy as np

directorio = r'd:\ambiente\escritorio\NotCode\Varios\03 Resoluciones MME - Cambio FPO'


daNames = []
daNambers = []
exepts = ['41333-17', '41332-17','41329-17','41330-17', '41486-17', '40844de', '41377-']

# Iterate directory
for path in os.listdir(directorio):
    # check if current path is a file
    if os.path.isfile(os.path.join(directorio, path)):
        daNames.append(path)
    daPieces = path.split(' ')
    # print(path)
    for aPiece in daPieces:
        if len(aPiece) == 5:
            ProbablyDaPiece = aPiece
            try:
                daPiece = int(ProbablyDaPiece)
                daNambers.append(str(daPiece))
                # print(daPiece)
            except:
                continue
        elif aPiece in exepts:
            daPiece = aPiece
            # print(daPiece)
            daNambers.append(daPiece)
            
daNames.remove('Thumbs.db')
print(len(daNambers))
print(len(daNames))

pathDF  = pd.DataFrame(daNames, index =daNambers,columns =['Path']).reset_index()
print(pathDF)

daNamesx = []
numbDF = pd.read_excel(r'd:\ambiente\escritorio\NotCode\Varios\ResSTN.xlsx') 
names = numbDF['NumeroRes'].values.tolist()

for name in names:
    daPartx = name.split(' ')
    # print(daPartx[0])
    daNamesx.append(daPartx[0])
# print(daNamesx)
NamesDF  = pd.DataFrame(names, index = daNamesx, columns =['Names']).reset_index()

print(NamesDF)

fullDF = pd.merge(NamesDF,pathDF, how = 'left', on = 'index')
fullDF['FullPath'] = r'\\archivosxm\TransaccionesdelMercado\LAC\STN\03 Expansión STN\03 Resoluciones MME - Cambio FPO' + '\\' + fullDF['Path']
del fullDF['Path']

fullDF.to_excel("ResSTNOut.xlsx")
