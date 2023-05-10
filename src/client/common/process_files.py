import csv

BATCH_SIZE = 1000


def update_count(count, log_func=None):
  """
  Update the count and log if necessary
  """
  PARTIAL_COUNT_LIM = 50000

  count["total"] += 1
  count["partial"] += 1

  if count["partial"] >= PARTIAL_COUNT_LIM:
    if log_func:
      log_func(count)
    count["partial"] = 0


def process_csv(file, process_fn, batch_size=BATCH_SIZE, limit=None, log_func=None):
  """
  Process a csv file in batches
  calling process_fn on each batch
  """

  line_count = {
      "total": 0,
      "partial": 0,
  }

  with open(file, 'r') as f:
    reader = csv.reader(f)

    # skip header row
    next(reader)

    # read lines lazily from file
    batch = []
    for row in reader:
      batch.append(row)
      if len(batch) == batch_size:
        process_fn(batch)
        batch = []

      update_count(line_count, log_func)
      if limit and line_count["total"] >= limit:
        break

    # process any remaining rows
    if batch:
      process_fn(batch)


def parse_weather_batch(rows):
  """
  Parse a list of lines of csv weather data
  Return in a string format, separating each row with a semicolon and each column with a comma
  Fields: date, precipitation (other fields are pruned)
  """
  def parse_row(row):
    # date,prectot,qv2m,rh2m,ps,t2m_range,ts,t2mdew,t2mwet,t2m_max,t2m_min,t2m,ws50m_range,ws10m_range,ws50m_min,ws10m_min,ws50m_max,ws10m_max,ws50m,ws10m,yearid
    return row[0] + "," + row[1]

  return ";".join([parse_row(row) for row in rows])


def parse_stations_batch(rows):
  """
  Parse a list of lines of csv station data
  Return in a string format, separating each row with a semicolon and each column with a comma
  Fields: year, code, lat, lng, name
  """
  def parse_row(row):
    # code,name,latitude,longitude,yearid
    return row[4] + "," + row[0] + "," + row[2] + "," + row[3] + "," + row[1]

  return ";".join([parse_row(row) for row in rows])


def parse_trips_batch(rows):
  """
  Parse a list of lines of csv trips data
  Return in a string format, separating each row with a semicolon and each column with a comma
  Fields: start_date,start_station_code,end_date,end_station_code,duration_sec,is_member,yearid
  """
  def parse_row(row):
    # start_date,start_station_code,end_date,end_station_code,duration_sec,is_member,yearid
    return ",".join(row)

  return ";".join([parse_row(row) for row in rows])
