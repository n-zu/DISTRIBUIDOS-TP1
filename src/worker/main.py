import logging
from common.setup import config, setup


def main():
    setup()

    logging.info("Worker Started")

    while True:
        string = config.sub_socket.recv_string()
        rows = string.split(";")
        logging.info(f"Received: {rows[0]}")


if __name__ == "__main__":
    main()
