SELECT /*+ NO_QUERY_TRANSFORMATION*/ SUM (a25enerh01 + a25enerh02 + a25enerh03 + a25enerh04 + a25enerh05 + a25enerh06 
+ a25enerh07 + a25enerh08 + a25enerh09 + a25enerh10 + a25enerh11 + a25enerh12 + a25enerh13 + a25enerh14 + a25enerh15 
+ a25enerh16 + a25enerh17 + a25enerh18 + a25enerh19 + a25enerh20 + a25enerh21 + a25enerh22 + a25enerh23 + a25enerh24) VALOR 
FROM LIQUIDACION.t25cenergia, t27cmodific a 
WHERE A.A27IDESUBIM <> A.A27IDESUBEX 
AND a.a27fecheven = (SELECT MAX (b.a27fecheven) FROM t27cmodific b 
WHERE b.a27fecheven <= a25fecha 
AND b.a27idencont = a.a27idencont) 
AND a25fecha >= to_date('2023-02-01', 'yyyy-mm-dd') 
AND a25fecha <= to_date('2023-02-28', 'yyyy-mm-dd') 
AND a25idencont NOT IN (SELECT b.idencont FROM sit_conatributos b 
WHERE b.valostri = 'FRTIE'
AND b.idatributo = 'FRTIE' 
AND b.fechinic = (SELECT MAX (c.fechinic) FROM sit_conatributos c 
WHERE c.fechinic <= sysdate 
AND (c.fechfina >= sysdate OR c.fechfina IS NULL) 
AND c.idatributo = b.idatributo 
AND c.idencont = b.idencont)) 
AND a.a27idencont = a25idencont 
AND a.a27idesubim = 'STN' 
AND a.a27estado = 'A'