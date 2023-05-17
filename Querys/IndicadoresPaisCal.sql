WITH ind AS (
	SELECT * FROM [BDSDL].[cal].[CalculoResultado] 
), ind_lec AS (
	SELECT fechaTrabajo, agenteID, MdoComer, nombreVariable, valor 
	FROM ind
	LEFT JOIN [BDSDL].[dbo].[AgenteCalidad] AS ag
		ON ind.agenteCalidadID = ag.agenteCalidadID
	LEFT JOIN [BDSDL].[dbo].[Variable] AS va
		ON ind.variableID = va.variableID
), pvt_ind AS (
SELECT fechaTrabajo, agenteID, MdoComer,[TotalConsumidores], [TotalConsumidoresAfectados], [SAIDI], [SAIFI], [TotalConsumidores]*[SAIDI] AS NUM_SAIDI, [TotalConsumidores]*[SAIFI] AS NUM_SAIFI 
FROM ind_lec
PIVOT( 
	MAX (valor)
	FOR nombreVariable IN ([TotalConsumidores], [TotalConsumidoresAfectados], [SAIDI], [SAIFI])
) AS pvt
)
--SELECT * FROM pvt_ind
SELECT fechaTrabajo as fecha, SUM(NUM_SAIDI)/SUM(TotalConsumidores) AS SAIDI_PAIS, SUM(NUM_SAIFI)/SUM(TotalConsumidores) AS SAIFI_PAIS FROM pvt_ind
GROUP BY fechaTrabajo

ORDER BY fechaTrabajo DESC