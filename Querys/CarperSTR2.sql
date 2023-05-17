WITH VariablesSTR AS(
	SELECT [documentoDetalleStrId]
      ,[documentoId]
      ,[str]
      ,[cd4Bruto]
      ,[cd4Neto]
      ,[demandaReal]
      ,[dt4Bruto]
      ,[dt4Neto]
  FROM [BDCargosPerdLAC].[CarPer].[DocumentoDetalleStr]
),
  Fechas AS (
	SELECT  [documentoId] AS DID2
      ,[fechaTrabajo]
	  ,[modulo]
	FROM [BDCargosPerdLAC].[CarPer].[Documento]
)

SELECT fechaTrabajo
      ,[cd4Neto] AS CD4STR2
      ,[demandaReal] AS DemandaSTR2
      ,[dt4Neto] AS DT4STR2
FROM VariablesSTR

LEFT JOIN Fechas
	ON VariablesSTR.documentoId = Fechas.DID2

WHERE dt4Bruto != 0
	AND dt4Neto != 0
	AND STR = 'Are0044'
ORDER BY fechaTrabajo DESC