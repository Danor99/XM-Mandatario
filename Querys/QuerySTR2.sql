WITH Documentos AS (
	SELECT fechaTrabajo, documentoId, tipo
	FROM [CarPer].[Documento]
	WHERE tipo = 7
),
PagosSTR AS (
	SELECT fechaTrabajo AS fechaTrabajo2, valor, porcentajeParticipacion, tipoRecibe, documentoId AS documentoId2
	FROM [CarPer].[DocumentoDetalleStrBalance]
	WHERE porcentajeParticipacion <> 0
	AND str = 2
)

SELECT fechaTrabajo,  FORMAT(SUM(valor), 'F1') AS SumaSTR2
FROM PagosSTR
LEFT JOIN Documentos
	ON Documentos.documentoId = PagosSTR.documentoId2
GROUP BY fechaTrabajo
ORDER BY fechaTrabajo DESC



