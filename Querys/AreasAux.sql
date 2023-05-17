SELECT [objID] as MercadoID
      ,[ultNombre] as Mercado
  FROM [BDMIDXM].[dbo].[MaestroObj]
  WHERE (objID LIKE 'Are%') OR (objID LIKE 'Aom%')