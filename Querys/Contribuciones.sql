-- CONTRIBUCIONES TOTALES POR FONDO

SELECT CONT.FECHA, CONT.FAER, CONT.PRONE, CONT.FOES, ENER_T.ENER_T
FROM
(
SELECT Ig.fechinic FECHA, SUM(Ig.FAER + Ig.FAER_VG) FAER, SUM(Ig.PRONE + Ig.PRONE_VG) PRONE, SUM(Ig.FOES + Ig.FOES_VG) FOES  FROM
(
SELECT  ing.fechinic, NVL(SUM(DECODE(ing.codigocto,088,ing.valor)),0) FAER, NVL(SUM(DECODE(ing.codigocto,089,ing.valor)),0) FAER_VG, NVL(SUM(DECODE(ing.codigocto,112,ing.valor)),0) PRONE, NVL(SUM(DECODE(ing.codigocto,113,ing.valor)),0) PRONE_VG,
NVL(SUM(DECODE(ing.codigocto,150,ing.valor)),0) FOES, NVL(SUM(DECODE(ing.codigocto,151,ing.valor)),0) FOES_VG
FROM
(SELECT fechinic, codigocto, VALOR FROM liquidacion.ict_agnresucarg a
where 1=1
  and codigoneg = '02'
  and idaplicacion = 'CALCARSTN'
  and Idmodulo in ('CALCARFACT')

  and codigocto in ('088','089','112','113','150','151')
  and version = 0
  order by fechinic) ing
group by ing.fechinic
order by fechinic
) Ig
group by Ig.fechinic,  Ig.FAER, Ig.FAER_VG, Ig.PRONE, Ig.PRONE_VG, Ig.FOES, Ig.FOES_VG
order by Ig.fechinic
) CONT

INNER JOIN

(
SELECT TRUNC(a25fecha,'MM') FECHA, SUM (a25enerh01 + a25enerh02 + a25enerh03 + a25enerh04 +  a25enerh05 + a25enerh06 + a25enerh07 + a25enerh08 +  a25enerh09 + a25enerh10
	+ a25enerh11 + a25enerh12 +  a25enerh13 + a25enerh14 + a25enerh15 + a25enerh16 +  a25enerh17 + a25enerh18 + a25enerh19 + a25enerh20 +   a25enerh21
 + a25enerh22 + a25enerh23 + a25enerh24) ENER_T
FROM LIQUIDACION.t25cenergia, t27cmodific a   WHERE A.A27IDESUBIM <> A.A27IDESUBEX
AND a.a27fecheven = (SELECT MAX (b.a27fecheven)
FROM t27cmodific b    WHERE b.a27fecheven <= a25fecha   AND b.a27idencont = a.a27idencont)
AND a25idencont NOT IN (SELECT b.idencont FROM sit_conatributos b  WHERE b.valostri = 'FRTIE'
AND b.idatributo = 'FRTIE'   AND b.fechinic = (SELECT MAX (c.fechinic)   FROM sit_conatributos c   WHERE c.fechinic <= sysdate
AND (c.fechfina >= sysdate OR c.fechfina IS NULL)  AND c.idatributo = b.idatributo   AND c.idencont = b.idencont))
AND a.a27idencont = a25idencont
AND a.a27idesubim = 'STN'
AND a.a27estado = 'A'
GROUP BY TRUNC(a25fecha,'MM')
ORDER BY 1 DESC
) ENER_T
ON ENER_T.FECHA = CONT.FECHA
