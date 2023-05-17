/*Declare @FI as date
Declare @FF as date
Declare @agente varchar(10)
Declare @tipo as int
Set @FI = '2020-07-01'
Set @FF ='2020-07-01'
Set @agente = 'Ung0141'
Set @tipo = 1*/

Select Doc.fechatrabajo, det.unidadNegocioOr, det.ventaUsuaConectadosStn, 
det.ventaComNoIncumbente, det.ventaComIncumbente, det.numeroMesesAjuste ,  det.ajusteCargo,
det.cargoRemunPGP--, doc.tipo --, det.cargoDevIng_RemunPGP
from CarPer.DocumentoDetallePerdidas det
left join CarPer.Documento Doc on det.documentoId = Doc.documentoId
where
det.unidadNegocioOr = @agente
and fechaTrabajo >= @FI
and fechaTrabajo <= @FI
and modulo = 2
and Doc.tipo = @tipo
and Doc.estado = 1
--and Doc.tipo = (Select max(tipo) from CarPer.Documento b where doc.fechaTrabajo = b.fechaTrabajo) --and doc.fechaTrabajo = b.fechaTrabajo
order by 4, 1