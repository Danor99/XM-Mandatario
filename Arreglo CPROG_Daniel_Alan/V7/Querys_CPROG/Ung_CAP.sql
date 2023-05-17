--Declare @agente varchar(10)
--Set @agente = 'Ung0029'

Select CVV1.unidadNegocio, CVV1.valor CAP
from CarPer.VariableValor CVV1
where
CVV1.variableId = '130'
and CVV1.unidadNegocio in (:Ungs)--('Ung0141','Ung0538','Ung0037','Ung0093','Ung0029','Ung0180','Ung0061','Ung0983')