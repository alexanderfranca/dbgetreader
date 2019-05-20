#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import re
import pprint

class DBGETReader:
    """
    Uses DBGET to read raw DBGET file entries, parse that and returns well formed dictionaries.
    """

    def __init__(self, reader=None):

        self.dbget = reader 

        self.entry = {}

    def entries_position(self):
        """
        Returns the entries position of the DBGET file.

        Entry position is the actual char that starts an entry in the file.
        """

        self.dbget.generate_entries_position()

        return self.dbget.get_entries_position()

    def parsed_entry(self, offset=None):
        """
        Return the entry in a dictonary format where entries from DBGET file left columns are keys and right columns are values.
        """

        formated_entry = {}
        entry = {}
        entry = self.dbget.get_entry_data(offset)

        for key, values in entry.items():
            for entry_name, entry_value in values.items():
                formated_entry[entry_name] = entry_value

        return formated_entry

    def all_entries(self):
        """
        Returns a list with all entries from a DBGET file.

        You'll use that only if you really know the time spent and RAM memory necessary to load all the entries from a DGET file.

        Big files will ruin your expectations. What is a 'big file'? Well... you have to do math concerning your context.
        """

        entries = []
        formated_entry = {}

        self.dbget.generate_entries_position()
        positions = self.dbget.get_entries_position()

        for position in positions:
            entry = self.dbget.get_entry_data(position)

            # Entry shouldn't be a list  but a simple dictionary, so we're
            # getting the dictionary out of the list (using [0])
            entries.append(list(entry.values()))

        # This is a SHIT workaround to remove items from its lists place.
        # Please, do something better.
        # The case here is: values() method returns a dict_values view. 
        # And that crazy thing doesn't allow string referencing.
        # So... put the result in a list solve the problem.
        # But... put a single structure in a list receptacle, what is stupid.
        # The code below only remove the items from its receptacle.
        tmp_entries = []
        for entry in entries:
            tmp_entries.append(entry[0])

        entries = []
        entries = tmp_entries

        return entries
