--Declare @FI as date
--Declare @FF as date
--Declare @agente varchar(10)
--Set @FI = '2019-05-01'
--Set @FF ='2020-03-01'
--Set @agente = 'Ung0029'

SELECT Fecha, valor IPP
FROM BDMIDXM.dbo.Variables 
WHERE Variables.nombreVariable = 'IPP'
and Fecha in (:Fechas)

order by 1