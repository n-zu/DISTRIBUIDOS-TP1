
def ensure_correct_keys(*stats_list):
  for stats in stats_list:
    if "viajes_con_precipitacion_mayor_a_30mm" not in stats:
      stats["viajes_con_precipitacion_mayor_a_30mm"] = {}
    if "cantidad_de_viajes_2016_y_2017" not in stats:
      stats["cantidad_de_viajes_2016_y_2017"] = {}
    if "distancias_montreal" not in stats:
      stats["distancias_montreal"] = {}


def join_stats(stats1, stats2):

  ensure_correct_keys(stats1, stats2)

  join_viajes_con_precipitacion_mayor_a_30mm(stats1, stats2)
  join_cantidad_de_viajes_2016_y_2017(stats1, stats2)
  join_distancias_montreal(stats1, stats2)

  return stats1


def join_viajes_con_precipitacion_mayor_a_30mm(stats1, stats2):
  key = "viajes_con_precipitacion_mayor_a_30mm"
  for dia in stats2[key]:
    if dia not in stats1[key]:
      stats1[key][dia] = stats2[key][dia]
    else:
      duracion_acumulada, cantidad_viajes = stats2[key][dia]
      stats1[key][dia] = (stats1[key][dia][0] + duracion_acumulada,
                          stats1[key][dia][1] + cantidad_viajes)


def join_cantidad_de_viajes_2016_y_2017(stats1, stats2):
  key = "cantidad_de_viajes_2016_y_2017"

  for ciudad in stats2[key]:
    if ciudad not in stats1[key]:
      stats1[key][ciudad] = stats2[key][ciudad]
      continue

    for estacion in stats2[key][ciudad]:
      if estacion not in stats1[key][ciudad]:
        stats1[key][ciudad][estacion] = stats2[key][ciudad][estacion]
        continue

      cantidad_viajes_2016, cantidad_viajes_2017 = stats2[key][ciudad][estacion]
      stats1[key][ciudad][estacion] = (stats1[key][ciudad][estacion][0] + cantidad_viajes_2016,
                                       stats1[key][ciudad][estacion][1] + cantidad_viajes_2017)


def join_distancias_montreal(stats1, stats2):
  key = "distancias_montreal"

  for estacion in stats2[key]:
    if estacion not in stats1[key]:
      stats1[key][estacion] = stats2[key][estacion]
    else:
      distancia_acumulada, cantidad_viajes = stats2[key][estacion]
      stats1[key][estacion] = (stats1[key][estacion][0] + distancia_acumulada,
                               stats1[key][estacion][1] + cantidad_viajes)
