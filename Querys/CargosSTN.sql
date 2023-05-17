SELECT Cargos.fechinic, SUM(DECODE(Cargos.codigocto,038,Cargos.valor)) T_neto_Maxima, SUM(DECODE(Cargos.codigocto,039,Cargos.valor)) T_neto_Media, SUM(DECODE(Cargos.codigocto,040,Cargos.valor)) T_neto_Minima, SUM(DECODE(Cargos.codigocto,037,Cargos.valor)) T_neto_Monomio
FROM
	(
	SELECT fechinic, CODIGOCTO, VERSION, VALOR FROM liquidacion.ict_resucarg a
		where 1=1
  	and codigoneg = '02'
  	and idaplicacion = 'CALCARSTN'
  	and Idmodulo in ('CALCARFACT')
  	and codigocto in ('037', '038', '039', '040')
  	and version ='0'

  ) Cargos
group by fechinic
order by 1 desc
-- CodigoCto 037 T' monomio
-- CodigoCto 038 T' maxima
-- CodigoCto 039 T' media
-- CodigoCto 040 T' minima
