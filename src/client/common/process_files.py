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

    # skip header row
    next(f)

    # read lines lazily from file
    batch = []
    for row in f:
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

def join_batch(rows):
  """
  Join a list of lines separated by semicolons
  """
  return ";".join(rows)
