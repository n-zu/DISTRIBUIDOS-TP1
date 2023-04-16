from common.setup import setup
from common.upload_data import upload_weather
from time import sleep


def main():
    setup()

    upload_weather()

    # upload_stations()

    # stream_trips()

    # get_stats()


if __name__ == "__main__":
    main()
