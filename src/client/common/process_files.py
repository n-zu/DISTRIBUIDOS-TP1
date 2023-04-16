import csv

BATCH_SIZE = 50


def process_csv(file, process_fn, batch_size=BATCH_SIZE):
    """
    Process a csv file in batches
    calling process_fn on each batch
    """
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
