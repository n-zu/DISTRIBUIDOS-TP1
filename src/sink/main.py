from common.setup import setup
from common.receive_stats import receive_stats, stats
from common.process_stats import process_stats
from common.communication import send_to_client


def main():
  setup()

  receive_stats()

  final_stats = process_stats(stats)
  send_to_client(final_stats)


if __name__ == "__main__":
  main()
