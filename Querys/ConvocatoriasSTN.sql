WITH ConvocatoriaAnualidad AS (
SELECT [convocatoriaID] AS ConvocatoriaID1
      ,[fechaIni] AS FechaInicial1
      ,[fechaFin] AS FechaFinal1
      ,[numero] 
      ,[valor]
FROM LqSTN.PeriodoConvocatoria
), ConvocatoriaDetalle AS (
SELECT [objID]
      ,[nombre]
      ,[descripcion]
      ,[resolucionCREG]
FROM LqSTN.Convocatoria
)

SELECT ConvocatoriaID1, FechaFinal1, FechaFinal1, numero, nombre, descripcion, resolucionCREG
FROM ConvocatoriaAnualidad

LEFT JOIN ConvocatoriaDetalle
	ON ConvocatoriaAnualidad.ConvocatoriaID1 = ConvocatoriaDetalle.objID

WHERE  FechaInicial1 < '2200-01-01'
	AND FechaFinal1 < '2200-01-01'

ORDER BY FechaInicial1 DESC