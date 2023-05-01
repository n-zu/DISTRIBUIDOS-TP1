from copy import deepcopy
from worker.common.static_data import handle_static_data
from worker.common.store import weather, stations
from worker.common.trips.trip import Trip
from worker.common.trips.process_trips import process_trip
from worker.common.trips.stats import stats
from sink.common.join_stats import join_stats
from sink.common.process_stats import process_stats

print("Testing static data")

static_data = [
    {
        "data_type": "weather",
        "city": "montreal",
        "rows": [
            # "date,prectot",
            "2020-01-01,10.0",
            "2020-01-02,20.0",
            "2020-01-03,30.0",
            "2020-01-04,40.0",
            "2020-01-05,50.0",
        ]
    },
    {
        "data_type": "stations",
        "city": "montreal",
        "rows": [
            # "code, lat, lng, year",
            "2020,001,0.0,0.0",
            "2020,002,0.0,100.0",
            "2020,003,100.0,0.0",
            "2020,004,100.0,100.0",
        ]
    }
]

for data in static_data:
  handle_static_data(data["data_type"], data["city"], data["rows"])

print("------WEATHER------")
print(weather)
print("------STATIONS------")
print(stations)

trips = [
    # city, start_date, start_station_code, end_date, end_station_code, duration_sec, is_member, yearid
    Trip("montreal", "2020-01-01 00:00:00", "001",
         "2020-01-01 01:00:00", "002", 3600, True, "2020"),
    Trip("montreal", "2020-01-02 00:00:00", "001",
         "2020-01-02 01:00:00", "002", 3600, True, "2020"),
    Trip("montreal", "2020-01-03 00:00:00", "001",
         "2020-01-03 01:00:00", "002", 3600, True, "2020"),
    Trip("montreal", "2020-01-04 00:00:00", "001",
         "2020-01-04 01:00:00", "002", 3600, True, "2020"),
    Trip("montreal", "2020-01-05 00:00:00", "001",
         "2020-01-05 01:00:00", "002", 3600, True, "2020"),
]

for trip in trips:
  process_trip(trip)

print("------STATS------")
print(stats)

stats1 = deepcopy(stats)
stats2 = deepcopy(stats)

joined_stats = join_stats(stats1, stats2)

print("------STATS x2------")
print(joined_stats)

processed_stats = process_stats(joined_stats)

print("------PROCESSED STATS------")
print(processed_stats)
