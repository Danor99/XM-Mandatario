WITH Variables AS(
	SELECT [documentoDetalleSdlId]
      ,[documentoId]
      ,[unidadNegocio]
      ,[CD3NetoSTR01]
      ,[CD3NetoSTR02]
      ,[CD32NetoSTR01]
      ,[CD32NetoSTR02]
      ,[CD2NetoSTR01]
      ,[CD2NetoSTR02]
      ,[cargUsoN1STR01]
      ,[cargUsoN1STR02]
      ,[cargUsoN2STR01]
      ,[cargUsoN2STR02]
      ,[cargUsoN3STR01]
      ,[cargUsoN3STR02]
      ,[CD4NetoSTR01]
      ,[CD4NetoSTR02]
      ,[energiaLiquidacionN1]
      ,[energiaLiquidacionN2]
      ,[energiaLiquidacionN3]
      ,[liquidacionCargosN1]
      ,[liquidacionCargosN2]
      ,[liquidacionCargosN3]
      ,[UnidadNegocioComercializador]
  FROM [BDCargosPerdLAC].[CarPer].[DocumentoDetalleSdl]
 ),
  Fechas AS (
	SELECT  [documentoId] AS DID2
      ,[fechaTrabajo]
	  ,[tipo]
	  ,[descripcion]
	FROM [BDCargosPerdLAC].[CarPer].[Documento]
		WHERE modulo = 0
)
SELECT fechaTrabajo AS Fecha
	  ,[tipo] AS Tipo
      ,[unidadNegocio] AS MercadoID
      ,[UnidadNegocioComercializador] AS numComercializador
	  ,(cargUsoN1STR01 + cargUsoN1STR02) AS DtNT1
	  ,(cargUsoN2STR01 + cargUsoN2STR02) AS DtNT2
	  ,(cargUsoN3STR01 + cargUsoN3STR02) AS DtNT3
      ,[energiaLiquidacionN1] AS EnergiaLiquidacionN1
      ,[energiaLiquidacionN2] AS EnergiaLiquidacionN2
      ,[energiaLiquidacionN3] AS EnergiaLiquidacionN3
      ,[liquidacionCargosN1] AS CargoLiquidacionN1
      ,[liquidacionCargosN2] AS CargoLiquidacionN2
      ,[liquidacionCargosN3] AS CargoLiquidacionN3
FROM Variables
LEFT JOIN Fechas
	ON Variables.documentoId = Fechas.DID2


WHERE fechaTrabajo is not NULL 
	AND UnidadNegocioComercializador is NULL
	AND energiaLiquidacionN1 is not NULL
	AND (tipo = 4) OR (tipo = 6) 

ORDER BY fechaTrabajo DESC, MercadoID