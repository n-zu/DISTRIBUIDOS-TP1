## Design Decisions

- Stations are identified by their city, yearid and code.
- Null treatment:
  - A trip with an unknown station is not considered for the avg dist statistic.
  - A trip in a day with unknown weather is not considered for the avg duration w/ prec>30mm statistic.
