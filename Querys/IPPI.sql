
SELECT A302FECHA FECHA, A302VALOR IPPI
FROM T302VALORESINDICADORES
WHERE 1=1
AND A302IDINDICADOR = 95
AND A302CONSECUTIVO = 1
ORDER BY FECHA DESC
