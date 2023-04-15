import csv

BATCH_SIZE = 50


def process_csv(file, process_fn, batch_size=BATCH_SIZE):
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
