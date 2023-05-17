Select CONCAT(map.bdmem, ' - ', SUBSTRING ( ung.nombreCorto,0, charindex('- D',ung.nombreCorto) )) nombreCorto, SUBSTRING ( ung.nombre,0, charindex('- DISTRIBUIDOR',ung.nombre)) nombre, ung.objID
from UnidadNegocio ung
left join mapeo map on map.objid = ung.objid
where 1=1
and ung.objId in (:Agentes)
and ung.fechaFin is NULL