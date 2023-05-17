select IngADD.AD AS 'ADD', IngADD.NT, IngADD.Fecha, IngR.IngR, IngADD.IngADD from 
(Select m.ultNombre 'AD', ad.fechaini 'Fecha', ad.NivelTension 'NT', sum(AD.Valor) IngADD from ResultadosCargosADD AD
inner join maestroobj m on m.objid = AD.area

where AD.Texto = 'IngADD'
and AD.ComercializadorID = 'UngZ' 
and AD.FechaIni >= '2008-01-01 00:00:00.000'
and AD.Version in ( select max(ver.version) from ResultadosCargosADD ver where ver.Texto = AD.texto and  ver.ComercializadorID = ad.ComercializadorID and ver.FechaIni = AD.FechaIni and ver.NivelTension = ad.NivelTension and ver.Area = ad.Area)
and AD.Estado in ( select max(est.Estado) from ResultadosCargosADD est where est.Texto = AD.texto and  est.ComercializadorID = AD.ComercializadorID and est.FechaIni = AD.FechaIni and est.NivelTension = ad.NivelTension and est.Area = ad.Area and est.Version = ad.Version)
group by m.ultNombre, ad.fechaini, ad.NivelTension
) IngADD

inner join 
(
select m2.ultNombre 'AD', IR.fechaini 'Fecha', IR.NivelTension 'NT', sum(IR.Valor) IngR  from ResultadosCargosADD IR
inner join maestroobj m2 on m2.objid = IR.area

where 1=1
and IR.Texto = 'IngR'
and IR.ComercializadorID = 'UngZ' 
and IR.FechaIni >= '2008-01-01 00:00:00.000'
and IR.Version in ( select max(ver2.version) from ResultadosCargosADD ver2 where ver2.Texto = IR.texto and  ver2.ComercializadorID = IR.ComercializadorID and ver2.FechaIni = IR.FechaIni and ver2.NivelTension = IR.NivelTension and ver2.Area = IR.Area)
and IR.Estado in ( select max(est2.Estado) from ResultadosCargosADD est2 where est2.Texto = IR.texto and  est2.ComercializadorID = IR.ComercializadorID and est2.FechaIni = IR.FechaIni and est2.NivelTension = IR.NivelTension and est2.Area = IR.Area and est2.Version = IR.Version)
group by m2.ultNombre, IR.fechaini, IR.NivelTension) IngR

on IngADD.AD = IngR.AD  and IngADD.NT = IngR.NT AND IngADD.Fecha = IngR.Fecha

order by 3 DESC
