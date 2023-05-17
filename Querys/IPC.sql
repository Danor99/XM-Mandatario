SELECT t302valoresindicadores.a302fecha FECHA, T302VALORESINDICADORES.A302VALOR IPC
FROM BASICAS.T301INDICADORES T301INDICADORES, BASICAS.T302VALORESINDICADORES T302VALORESINDICADORES
WHERE T301INDICADORES.A301IDINDICADOR = T302VALORESINDICADORES.A302IDINDICADOR
AND (T301INDICADORES.A301NOMBRE='IPC')
AND A301CONSECUTIVO = 1
ORDER BY FECHA DESC
