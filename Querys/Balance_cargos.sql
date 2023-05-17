
SELECT COM.FECHA, COM.VALOR COMERCIALIZADORES, GEN.VALOR  GENERADORES, TN.VALOR TRANSMISORES, XMII.VALOR XMII
FROM
(SELECT COMER.FECHADESDE FECHA, SUM(COMER.VALOR) VALOR
FROM
(
SELECT  LFT_MVTOSDOCUMENTOS.FECHADESDE,  SUM(LFT_MVTOSDOCUMENTOS.VALORDTO) VALOR
FROM LAC.LFT_MVTOSDOCUMENTOS LFT_MVTOSDOCUMENTOS
WHERE 1=1
AND LFT_MVTOSDOCUMENTOS.ESTADOREG='DISTRIBUID'
AND IDENTAGENT LIKE ('%C')
AND NROREFACT='0'
GROUP BY LFT_MVTOSDOCUMENTOS.FECHADESDE

UNION ALL

SELECT a.fechinic, SUM(DECODE(a.codigocto,146,a.valor)) PPA
  FROM liquidacion.ict_agnresucarg a
      where 1=1
      and a.codigoneg ='02'
      and a.Idaplicacion = 'CALCARSTN'
      and a.Idmodulo in ('CALCARFACT')
      and a.identagent not like ('%T')
      and a.Codigocto in ('075','076','077','109','146')
      and a.version = '0'
      group by a.fechinic
) COMER
GROUP BY COMER.FECHADESDE
) COM

LEFT JOIN
(
SELECT  LFT_MVTOSDOCUMENTOS.FECHADESDE,  SUM(LFT_MVTOSDOCUMENTOS.VALORDTO) VALOR
FROM LAC.LFT_MVTOSDOCUMENTOS LFT_MVTOSDOCUMENTOS
WHERE 1=1
AND LFT_MVTOSDOCUMENTOS.ESTADOREG='DISTRIBUID'
	AND IDENTAGENT LIKE ('%G')
AND NROREFACT='0'
GROUP BY LFT_MVTOSDOCUMENTOS.FECHADESDE
) GEN
ON  COM.FECHA = GEN.FECHADESDE
INNER JOIN
(
SELECT TN.FECHADESDE FECHA, SUM(TN.VALOR) VALOR
FROM
(
SELECT  LFT_MVTOSDOCUMENTOS.FECHADESDE,  SUM(LFT_MVTOSDOCUMENTOS.VALORDTO) VALOR
FROM LAC.LFT_MVTOSDOCUMENTOS LFT_MVTOSDOCUMENTOS
WHERE 1=1
AND LFT_MVTOSDOCUMENTOS.ESTADOREG='DISTRIBUID'
	AND IDENTAGENT LIKE ('%T')
AND NROREFACT='0'
GROUP BY LFT_MVTOSDOCUMENTOS.FECHADESDE

UNION ALL

SELECT a.fechinic, SUM(DECODE(a.codigocto,146,a.valor)) PPA
  FROM liquidacion.ict_agnresucarg a
      where 1=1
      and a.codigoneg ='02'
      and a.Idaplicacion = 'CALCARSTN'
      and a.Idmodulo in ('CALCARFACT')
      and a.identagent like ('%T')
      and a.Codigocto in ('075','076','077','109','146')
      and a.version = '0'
      group by a.fechinic
) TN
GROUP BY TN.FECHADESDE
) TN
ON TN.FECHA = COM.FECHA

LEFT JOIN

(
SELECT  LFT_MVTOSDOCUMENTOS.FECHADESDE FECHA,  SUM(LFT_MVTOSDOCUMENTOS.VALORDTO) VALOR
FROM LAC.LFT_MVTOSDOCUMENTOS LFT_MVTOSDOCUMENTOS
WHERE 1=1
AND LFT_MVTOSDOCUMENTOS.ESTADOREG='DISTRIBUID'
	AND IDENTAGENT = 'XMII'
AND NROREFACT='0'
GROUP BY LFT_MVTOSDOCUMENTOS.FECHADESDE
) XMII
ON XMII.FECHA = COM.FECHA
ORDER BY FECHA DESC
