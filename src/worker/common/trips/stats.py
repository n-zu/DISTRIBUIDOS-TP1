from .trip import Trip
import middleware
import json
import logging

stats = {
    "viajes_con_precipitacion_mayor_a_30mm": {
        # "dia" : (duracion_acumulada, cantidad_viajes), ...
    },
    "cantidad_de_viajes_2016_y_2017": {
        # "ciudad" : {
        #   "estacion_inicio": (cantidad_viajes_2016, cantidad_viajes_2017), ...
        # }, ...
    },
    "distancias_montreal": {
        # "estacion_fin": (distancia_acumulada, cantidad_viajes), ...
    }
}


def update_viajes_con_precipitacion_mayor_a_30mm(trip: Trip):
  key = "viajes_con_precipitacion_mayor_a_30mm"
  if trip.precipitation < 30:
    return

  if not trip.duration_sec or trip.duration_sec is None:
    return

  if trip.start_date not in stats[key]:
    stats[key][trip.start_date] = (trip.duration_sec, 1)
  else:
    duracion_acumulada, cantidad_viajes = stats[key][trip.start_date]
    stats[key][trip.start_date] = (
        duracion_acumulada + trip.duration_sec, cantidad_viajes + 1)


def update_cantidad_de_viajes_2016_y_2017(trip: Trip):
  key = "cantidad_de_viajes_2016_y_2017"

  def get_year(date):
    return int(date.split('-')[0])

  year = get_year(trip.start_date)

  if year != 2016 and year != 2017:
    return

  if trip.city not in stats[key]:
    stats[key][trip.city] = {}

  if trip.start_station_code not in stats[key][trip.city]:
    stats[key][trip.city][trip.start_station_code] = (0, 0)

  cantidad_viajes_2016, cantidad_viajes_2017 = stats[key][trip.city][trip.start_station_code]
  if year == 2016:
    stats[key][trip.city][trip.start_station_code] = (
        cantidad_viajes_2016 + 1, cantidad_viajes_2017)
  else:
    stats[key][trip.city][trip.start_station_code] = (
        cantidad_viajes_2016, cantidad_viajes_2017 + 1)


def update_distancias_montreal(trip: Trip):
  key = "distancias_montreal"
  if trip.city != "montreal":
    return

  if not trip.distance or trip.distance is None:
    return

  if trip.end_station_code not in stats[key]:
    stats[key][trip.end_station_code] = (0, 0)

  distancia_acumulada, cantidad_viajes = stats[key][trip.end_station_code]
  stats[key][trip.end_station_code] = (
      distancia_acumulada + trip.distance, cantidad_viajes + 1)


def update_stats(trip: Trip):
  """Update statistics"""

  update_viajes_con_precipitacion_mayor_a_30mm(trip)
  update_cantidad_de_viajes_2016_y_2017(trip)
  update_distancias_montreal(trip)

def count_stats(stats):
  count = {}
  for key in stats:
    count[key] = len(stats[key])
  return count

def upload_stats():
  stats_msg = json.dumps(stats)
  middleware.push(stats_msg)
  logging.debug(f"Uploaded stats {count_stats(stats)}")
