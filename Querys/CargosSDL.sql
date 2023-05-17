WITH DT as (SELECT  [Area]
      ,[VariableID]
      ,[OperadorID]
      ,[FechaIni]
      ,[NivelTension]
      ,[Texto]
      ,[Valor] as DtUN
	  ,Version
	  ,Estado
  FROM [BDMIDXM].[dbo].[ResultadosCargosADD]
  WHERE VariableID = 'Res0051'
  AND Version = 1
  AND Estado = 4
),

DtUN as (SELECT  [Area] as Area2
      ,[VariableID] as VariableID2
      ,[OperadorID] as OperadorID2
      ,[FechaIni] as FechaIni2
      ,[NivelTension] as NivelTension2
      ,[Texto] as Texto2
      ,[Valor] as DT
  FROM [BDMIDXM].[dbo].[ResultadosCargosADD]
  WHERE VariableID = 'Res0059'
  AND Version = 1
  AND Estado = 4
),

Names1 as (SELECT [objID]
      ,[ultNombre] as NombreArea
      ,[tipoID]
      ,[ultVersion]
  FROM [BDMIDXM].[dbo].[MaestroObj]
  WHERE (objID LIKE 'Are%') OR (objID LIKE 'Aom%')
),

Names2 as (SELECT [objID]
      ,[ultNombre] as NombreMercado
      ,[tipoID]
      ,[ultVersion]
  FROM [BDMIDXM].[dbo].[MaestroObj]
  WHERE (objID LIKE 'Are%') OR (objID LIKE 'Aom%')
)

SELECT FechaIni as fecha, NombreArea as Area, NombreMercado as Mercado, NivelTension as NT, DtUN, DT
FROM DT
LEFT JOIN DtUN
	ON DT.FechaIni = DtUN.FechaIni2
	AND DT.Area = DtUN.Area2
	AND DT.NivelTension = DtUN.NivelTension2

LEFT JOIN Names1
	ON DT.Area = Names1.objID

LEFT JOIN Names2
	ON DtUN.OperadorID2 = Names2.objID

WHERE Version = 1
AND Estado = 4

ORDER BY FechaIni DESC, Area