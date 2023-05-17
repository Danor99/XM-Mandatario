Select nombre nombreCorto, nombre, objID 
from registrar.AgrupaORMercado
where 1=1
and objId in (:Agentes)
and fechaFin is NULL