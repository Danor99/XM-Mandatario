WITH VariablesCPROG AS (
	SELECT *
	FROM [BDCargosPerdLAC].[CarPer].[DocumentoDetallePerdidas]
),
	Fechas AS (
	SELECT [documentoId] AS documentoId2
      ,[fechaTrabajo]
      ,[estado]
      ,[tipo]
      ,[modulo]
  FROM [BDCargosPerdLAC].[CarPer].[Documento]
)

SELECT  fechaTrabajo AS fecha,
		unidadNegocioOr AS MercadoID,
		cargoRemunPGP AS CPROG


FROM VariablesCPROG
LEFT JOIN Fechas
	ON VariablesCPROG.documentoId = Fechas.documentoId2

WHERE estado = 2
AND tipo = 1

ORDER BY Fecha DESC