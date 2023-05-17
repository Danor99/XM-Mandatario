Select CONCAT(map.bdmem, ' - ', SUBSTRING ( ung.nombreCorto,0, charindex('- D',ung.nombreCorto) ),'Mercado de Comercialización ', aom.nombre) nombreCorto, aom.nombre nombre, ung.objID
from registrar.AgrupaORMercado aom
left join Birrelacion bir on bir.objid2 = aom.objid  and bir.objID = 'Bir0452' and bir.fechaFin is null
left join UnidadNegocio ung on ung.objid = bir.objid1 and ung.fechaFin is null
left join mapeo map on map.objid = ung.objid
where 1=1
and aom.objId in (:Agentes)
and aom.fechaFin is NULL
and aom.clasificacion = 'ActivosUso'

order by ung.objID