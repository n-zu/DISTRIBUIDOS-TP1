import logging
from .static.store import get_station


def add_station_name(city, id):
  name = get_station(city, id)
  if name is None:
    return id
  else:
    return f"{id}-{name}"


def process_stats(stats):

  processed_stats = {}

  key = "avg_duration_per_day_with_precipitation>30mm"
  processed_stats[key] = process_viajes_con_precipitacion_mayor_a_30mm(
      stats["viajes_con_precipitacion_mayor_a_30mm"])

  key = "estaciones_#viajes_2016_>=_2*#viajes_2017"
  processed_stats[key] = process_cantidad_de_viajes_2016_y_2017(
      stats["cantidad_de_viajes_2016_y_2017"])

  key = "estaciones_montreal_avgDist>=6"
  processed_stats[key] = process_distancias_montreal(
      stats["distancias_montreal"])

  logging.info("Processed stats")
  return processed_stats


def process_viajes_con_precipitacion_mayor_a_30mm(stats):
  result = {}
  for dia in stats:
    duracion_acumulada, cantidad_viajes = stats[dia]
    try:
      result[dia] = float(duracion_acumulada) / int(cantidad_viajes)
    except:
      logging.error(
          f"Error al procesar viajes_con_precipitacion_mayor_a_30mm: {duracion_acumulada}/{cantidad_viajes}")

  return result


COEF_2016v2017 = 2


def process_cantidad_de_viajes_2016_y_2017(stats):
  result = {}
  for ciudad in stats:
    result[ciudad] = []
    for station_id in stats[ciudad]:
      cantidad_viajes_2016, cantidad_viajes_2017 = stats[ciudad][station_id]
      try:
        if (int(cantidad_viajes_2017) >= COEF_2016v2017 * int(cantidad_viajes_2016)):
          station = add_station_name(ciudad, station_id)
          result[ciudad].append(station)
      except:
        logging.error(
            f"Error al procesar cantidad_de_viajes_2016_y_2017: {cantidad_viajes_2016}x2=={cantidad_viajes_2017}")

  return result


MIN_AVG_DIST = 6
MONTREAL = "montreal"


def process_distancias_montreal(stats):
  result = []
  for station_id in stats:
    distancia_acumulada, cantidad_viajes = stats[station_id]
    try:
      distancia_avg = float(distancia_acumulada) / int(cantidad_viajes)
      if float(distancia_avg) >= MIN_AVG_DIST:
        station = add_station_name(MONTREAL, station_id)
        result.append(station)
    except:
      logging.error(
          f"Error al procesar distancias_montreal: {distancia_acumulada}/{cantidad_viajes}")

  return result
