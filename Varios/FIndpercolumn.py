import pandas as pd

df = pd.read_excel('EDC.xlsx')

Position = []
Reference = []

Referencias = df['MLFB'].values.tolist()
Refes2 = [x for x in Referencias if str(x) != 'nan']

#print(Refes2)

Descripcion = df['Descripción Español'].values.tolist()
Descs2 = [x for x in Descripcion if str(x) != 'nan']

#print(Descs2)


for Refe2 in Refes2:
    for Desc2 in Descs2:
        if  Refe2 in Desc2:
            index = Descs2.index(Desc2) + 2
            Reference.append(Refe2)
            Position.append(index)

dff = pd.DataFrame(list(zip(Position, Reference)),
               columns =['Posicion', 'Referencia'])

dfff = dff.sort_values(by='Posicion')

print(dfff)
