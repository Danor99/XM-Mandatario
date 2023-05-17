/*Declare @FI as date
Declare @FF as date
Declare @agente varchar(10)
Declare @NMA int
Set @FI = '2020-04-01'
Set @FF ='2020-02-01'
Set @NMA = 10*/

Select insumos.Fecha Fecha, insumos.Valor_IPPm_2 Valor_IPPm_2,
insumos.MgVenta_UsConectadosSTNCargoPerdidas,
insumos.MgVentaComercializadorNoIncumbenteCargoPerdidas,
insumos.MgVentaComercializadorIncumbenteCargoPerdidas
from( 


Select IPP.Fecha Fecha, IPP.Valor_IPPm_2 Valor_IPPm_2, --sum(VenSTN.valor), sum(VenNoInc.valor), sum(VenInc.valor)
lag(sum(VenSTN.valor),3,0) over(order by IPP.Fecha) as  MgVenta_UsConectadosSTNCargoPerdidas,
lag(sum(VenNoInc.valor),3,0) over(order by IPP.Fecha) as  MgVentaComercializadorNoIncumbenteCargoPerdidas,
lag(sum(VenInc.valor),3,0) over(order by IPP.Fecha) as  MgVentaComercializadorIncumbenteCargoPerdidas

from	(
			SELECT Fecha, lag(Fecha,2,0) over(order by Fecha) as  m_2 , lag(Valor,2,0) over(order by Fecha)  Valor_IPPm_2
			FROM BDMIDXM.dbo.Variables 
			WHERE Variables.nombreVariable = 'IPP'
			and Fecha >= dateadd(m,-3,@FI)
			And Fecha <= @FI) IPP

left join [BDMIDXM].[Tmp].[DgpResultadosOR] VenInc on IPP.Fecha = VenInc.fechaVigencia 
		and VenInc.conceptoid in ('MgVentaComercializadorIncumbenteCargoPerdidas') 
		and VenInc.orID in('Ung0983','Ung0066')
		and VenInc.verID in (select max(verID) from [BDMIDXM].[Tmp].[DgpResultadosOR] b where VenInc.fechaVigencia = b.fechaVigencia and VenInc.orID = b.orID and VenInc.conceptoid = b.conceptoid)

left join [BDMIDXM].[Tmp].[DgpResultadosOR] VenSTN on IPP.Fecha = VenSTN.fechaVigencia 
		and VenSTN.conceptoid in ('MgVenta_UsConectadosSTNCargoPerdidas') 
		and VenSTN.orID = VenInc.orID
		and VenSTN.verID in (select max(verID) from [BDMIDXM].[Tmp].[DgpResultadosOR] b where VenSTN.fechaVigencia = b.fechaVigencia and VenSTN.orID = b.orID and VenSTN.conceptoid = b.conceptoid)



left join [BDMIDXM].[Tmp].[DgpResultadosOR] VenNoInc on IPP.Fecha = VenNoInc.fechaVigencia 
		and VenNoInc.conceptoid in ('MgVentaComercializadorNoIncumbenteCargoPerdidas')--,'MgVenta_UsConectadosSTNCargoPerdidas','MgVentaComercializadorIncumbenteCargoPerdidas')
--	and VenNoInc.fechaVigencia >= dateadd(m,-3,@FI)
--	and VenNoInc.fechaVigencia <= dateadd(m,-3,@FF)
	and VenNoInc.orID = VenInc.orID
	and VenNoInc.verID in (select max(verID) from [BDMIDXM].[Tmp].[DgpResultadosOR] b where VenNoInc.fechaVigencia = b.fechaVigencia and VenNoInc.orID = b.orID and VenNoInc.conceptoid = b.conceptoid)

where 1=1
and IPP.Fecha >= dateadd(m,-3,@FI)
And IPP.Fecha <= @FI
group by IPP.Fecha, IPP.Valor_IPPm_2
)insumos
where 1=1
and insumos.Fecha >= @FI
And insumos.Fecha <= @FI
order by 1

