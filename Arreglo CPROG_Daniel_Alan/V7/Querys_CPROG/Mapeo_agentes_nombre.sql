Select nombreCorto, nombre, objID 
from UnidadNegocio
where 1=1
and objId in (:Agentes)
and fechaFin is NULL