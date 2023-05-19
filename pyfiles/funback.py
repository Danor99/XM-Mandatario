## Realizar Grafica SDL Old

# def realizar_grafica_SDL(GraficaDF, AreaName = 'ADD Centro', ImgName = "No name", title = "No Title"):
#     df1 = (GraficaDF[(GraficaDF["Area"] == AreaName) & (GraficaDF["fecha"] >= Fecha_inicio) & (GraficaDF["fecha"] <= Fecha_final)]).sort_values(["fecha", "Mercado"], ascending = False)[["fecha", "Mes", "Mercado", "DT", "DtUN", "NT"]]

#     df11 = df1[df1["NT"] == '1'].reset_index()[["Mes", "Mercado", "DT", "DtUN"]].reset_index()
#     df12 = df1[df1["NT"] == '2'].reset_index()[["Mes", "Mercado", "DT", "DtUN"]].reset_index()
#     df13 = df1[df1["NT"] == '3'].reset_index()[["Mes", "Mercado", "DT", "DtUN"]].reset_index()
    

#     ax = df11.plot(x='index', y='DT', kind='scatter', c='#440099', label='DTUN1', marker = '.' , figsize = (8,5))
#     df12.plot(x='index', y='DT', kind='scatter', ax=ax, c='#FF6A13', label='DTUN2', marker = '.')
#     df13.plot(x='index', y='DT', kind='scatter', ax=ax, c='#75787B', label='DTUN3', marker = '.')

#     df11.plot(x='index', y='DtUN', kind='line', ax=ax, c='#440099', label='DT1')
#     df12.plot(x='index', y='DtUN', kind='line', ax=ax, c='#FF6A13', label='DT2')
#     df13.plot(x='index', y='DtUN', kind='line', ax=ax, c='#75787B', label='DT3')

#     max_dt = df11["DT"].max()
#     min_dt = df13["DT"].min()


#     if (AreaName == 'ADD Centro') | (AreaName == 'ADD Occidente'):
#         vlines_pos = [6.5, 13.5]
#         xticks = [3,10,17]
#     elif AreaName == 'ADD Sur':
#         vlines_pos = [5.5, 11.5]
#         xticks = [2,8.5,15]
#     elif AreaName == 'ADD Oriente':
#         vlines_pos = [4.5, 9.5]
#         xticks = [2,7,12]

#     if AreaName == 'ADD Occidente':
#         min_dt = df12["DT"].min()


#     plt.vlines(x = vlines_pos, ymin = min_dt, ymax = max_dt, color = 'black', linewidth = 1, linestyle = 'dashed')
#     xticks_lab = [mesesSTR[0], mesesSTR[1], mesesSTR[2]]
#     # ax.legend(bbox_to_anchor = (1.0, 1), loc = 'upper left')
#     plt.xticks(xticks, xticks_lab)
#     plt.xlabel("Mes")
#     plt.ylabel("Cargo por Uso")
#     plt.title(title)
#     plt.grid()
#     save = plt.savefig(r"Temp\{name}.png".format(name=ImgName))
    # return save