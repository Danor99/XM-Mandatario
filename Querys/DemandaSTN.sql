SELECT  FECHINIC,SUM(VALOR) AS DEMANDA_STN
FROM liquidacion.ict_agnresucarg
where codigoneg ='02'   
and Idaplicacion = 'CALCARSTN'  
and Idmodulo in ('CALCARESTI')    
and Codigocto in ('075','076','077')    
and fechinic > to_date ('2020-10-01','yyyy-mm-dd')
and version = '0'

GROUP BY(FECHINIC)
ORDER BY (FECHINIC) DESC