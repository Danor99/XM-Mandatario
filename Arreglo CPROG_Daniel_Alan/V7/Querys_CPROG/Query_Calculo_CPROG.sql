/*Declare @agente varchar(10)
Set @agente = 'Ung0538'*/

Select CVV1.unidadNegocio, CVV1.valor CAP, /*CVV2.valor EstadoPlan, CVV3.valor TipoPlan,*/ CVV4.valor IngTotalDev_RemunPGP  
from CarPer.VariableValor CVV1
left join CarPer.VariableValor CVV2 on CVV1.unidadNegocio = CVV2.unidadNegocio and CVV2.variableId = '190' 
left join CarPer.VariableValor CVV3 on CVV1.unidadNegocio = CVV3.unidadNegocio and CVV3.variableId = '139' 
left join CarPer.VariableValor CVV4 on CVV1.unidadNegocio = CVV4.unidadNegocio and CVV4.variableId = '156'
where
CVV1.variableId = '130'
and CVV1.unidadNegocio = @agente
and CVV1.fechafin is null
and CVV2.fechafin is null
and CVV3.fechafin is null
and CVV4.fechafin is null



