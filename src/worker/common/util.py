def parse_float(num):
  try:
    return float(num)
  except ValueError:
    return None
