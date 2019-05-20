# -*- coding: utf-8 -*-

# Import essential modules
from dbgetreader.dbgetreader import DBGETReader
from dbgetreader.dbget import DBGET

# Load the reader and load the dbgetreader
dbget = DBGET(file_to_read='./tests/fixtures/enzyme')
dbgetr = DBGETReader(reader=dbget)

# Get the positions from all the entries from the chosen file
positions = dbgetr.entries_position()

# Iterate through all the positions and get the entry for that position.
for position in positions:
    entry = dbgetr.parsed_entry(position)
    print(entry['ENTRY'][0])
