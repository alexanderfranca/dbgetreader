# -*- coding: utf-8 -*-

import os
import sys
import re
import pprint


class DBGET:
    """
    Parses a DBGET file and returns a dictionary containing every 'ENTRY' entry as a main key and all the other entries and values as that key values.

    Attributes:
        stop(int): A mark used to identify when an entry was done and the values has to be stored.
        times_entry_was_found(int): A counter used to identify when a new entry was found.
        entries(dict): This whole class is about filling that result dictionary.
        file_to_read(file): File handle that represents the DBGET file.
        main_entry_key(str): The 'ENTRY' entry value is the main key for each item in the dictionary.
        current_entry_key(str): Keep tracking of the current entry.
        entries_position(list): Stores all the entry positions from a DBGET file.

    """

    def __init__(self, file_to_read=None):

        # a mark used to identify when an entry was done and the values has to
        # be stored.
        self.stop = 0

        # a counter used to identify when a new entry was found.
        self.times_entry_was_found = 0

        # this whole class is about filling that result dictionary.
        self.entries = {}

        # the DBGET file.
        self.file_to_read = file_to_read

        # the 'ENTRY' entry value is the main key for each item in the
        # dictionary.
        self.main_entry_key = None

        # Keep tracking of the current entry the algorithm is reading. Important because we don't treat
        # the values. All the values will also have its entry name appended. Other classes/methods are
        # responsible to deal with key and values details (DBGET files is
        # specific for each use: enzyme, pathway, orthologs etc).
        self.current_entry_key = None

        # Stores all the entry positions from a DBGET file.
        entries_position = []

    def is_end_of_entry(self, string=None):
        """
        Returns if the string is a 'end of entry mark'.

        Entries from a DBGET file are delimited by a '///' string.

        Args:
            string(str): An string to be tested.

        Returns:
            (boolean): If the string marks an end of entry.
        """

        re_end = re.compile('///')

        if re_end.search(string):
            return True
        else:
            return False

    def get_entries_position(self):
        """
        Returns a list contatining all entries position (actual file character position) of every entry start.

        Returns:
            (list): List of entries positions.
        """

        return self.entries_position

    def generate_entries_position(self):
        """
        Generates a list of entry positions from a DBGET file.

        Entries positions means the char position of a entry start.
        """

        self.entries_position = []

        position = 0

        self.entries_position.append(0)

        with open(self.file_to_read) as file_to_read:
            for line in file_to_read:

                position = position + len(line.rstrip('\r\n')) + 1

                if self.is_end_of_entry(line):
                    self.entries_position.append(position)

        # We don't need the position of the end of the file.
        self.entries_position.pop()

    def get_entry_data(self, offset=None):
        """
        Returns a dictionary containing an entry with all left columns as keys and right columns as values.

        Args:
            offset(int): The position of the entry. It's gotten by the self.generate_entries_position() and self.get_entries_position() methods.

        Returns:
            (dict): The entry in a dictionary format.
        """

        # 9 hours until realize that this variable below should be reset. If not, that bastard still has previous stored value if you use DBGET class more then a single time in the same script, even in a different file.
        # Go fuck yourself 'self.entries'.
        # So, bug solved. Sorry for the pantomime.
        self.entries = {}

        # Reset the entry values.
        entry = {}

        # Get the DBGET file.
        with open(self.file_to_read) as f:

            f.seek(offset)

            # Looking forward lines that starts with uppercase chars, in other
            # words, uppercase chars that starts a line means a entry marker.
            re_keys = re.compile('^[A-Z].*')

            for line in f:

                # do the search for entry mark
                re_keys_result = re_keys.search(line)

                # if we found a entry mark
                if re_keys_result:

                    # clean/parse the result to get/store only the entry name
                    # value, like ENTRY, NAME, CLASS etc.
                    found_key = re_keys_result.group(0)
                    found_key = found_key.split(' ')
                    found_key = found_key[0]

                    # keep the entry key we're reading because it will be concatenated to its value inside the dictionary.
                    #self.current_entry_key = found_key

                # That's a special mark for the algorithm. Tells that an entry
                # block was entirely read.
                if self.stop == 1:
                    self.stop = 0

                # Creates the result from the method that parses the entry and its values.
                # That's the most important operation of this method we're
                # commenting.
                self.__parse_entry(line, found_key)

                # Found the end of an entry, so we simply exit the loop giving the
                # entry to the user.
                if self.is_end_of_entry(line):

                    # self.entries can store all the entries from a file. We don't
                    # need that, we want only the single entry parsed.
                    entry = self.entries

                    # reset self.entries to avoid duplications.
                    self.entries = {}

                    # Gives the entry data.
                    return entry

    def whole_file_data(self):
        """
        Run through the DBGET file and generates a dictionary containing all the entries.

        You will use this method ONLY if you are sure about the execution time and available RAM memory to load your entire file.

        Returns:
            (dict): dictionary containing all the entries from the DBGET file.

        """

        # Looking forward lines that starts with uppercase chars, in other
        # words, uppercase chars that starts a line means a entry marker.
        re_keys = re.compile('^[A-Z].*')

        with open(self.file_to_read) as f:
            for line in f:
                # do the search for entry mark
                re_keys_result = re_keys.search(line)

                # if we found a entry mark
                if re_keys_result:

                    # clean/parse the result to get/store only the entry name
                    # value, like ENTRY, NAME, CLASS etc.
                    found_key = re_keys_result.group(0)
                    found_key = found_key.split(' ')
                    found_key = found_key[0]

                    # keep the entry key we're reading because it will be concatenated to its value inside the dictionary.
                    #self.current_entry_key = found_key

                # That's a special mark for the algorithm. Tells that an entry
                # block was entirely read.
                if self.stop == 1:
                    self.stop = 0

                # Creates the result from the method that parses the entry and its values.
                # That's the most important operation of this method we're
                # commenting.
                self.__parse_entry(line, found_key)

        return self.entries

    def __parse_entry(self, line=None, entry=None):
        """
        Uses class variables as tracking and status. Dependent of other class methods execution.

        Pick a text line and search for entry marks and entry values. Depending on what it founds, generate the
        entry keys and values.

        Returns:
            (void): it only append to the class dictionary self.entries the parsed values from the DBGET file.

        """

        # Will store the value from a entry.
        entry_value = ''

        # looking forward entries marks, like ENTRY, NAME, CLASS etc
        re_new_entry_record = re.compile('^[A-Z]')

        # looking forward the specific entry mark. It means, if we found a REACTION entry in the caller method, we have to keep it
        # for distinguish between a general entry (CLASS, NAME, DBLINKS etc)
        # and the specific entry we're reading.
        re_specific_entry = re.compile('^' + entry)

        # If we found a entry, we have to count. If we have two entries, it means we reached a new entry, in other words, we have
        # to finish storing the previously entry and start a new reading.
        if re_new_entry_record.search(line):
            self.times_entry_was_found = self.times_entry_was_found + 1

        # Read the comment above.
        if self.times_entry_was_found > 1:
            self.times_entry_was_found = 1
            self.stop = 1

        re_specific_entry_result = re_specific_entry.search(line)

        # It means we are in the first value of the entry, in other words, something like 'CLASS    Oxireductases;'.
        # So, we take care of the entry key (like picking the 'CLASS' word from
        # the line) and treat the value
        if re_specific_entry_result:

            # Abnormally important: we have to keep tracking of the current entry mark we're reading.
            # It will be used as a subkey in the dictionary.
            self.current_entry_key = entry

            # When we find an entry in a DBGET file, we have to treat its
            # value.
            entry_record = re.compile('^([A-Z_]{1,}\s{1,})(.*)$')
            entry_record = entry_record.search(line)
            entry_value = entry_record.group(2)
            entry_value = entry_value.rstrip('\r\n')

            # 'ENTRY' is a special entry mark. Means the main key of the dictionary.
            # This method is all about picking the lines from a DBGET file and put all
            # the lines nested to its 'ENTRY' entry.
            if re_specific_entry_result.group(0) == 'ENTRY':

                # We reached a new (or the first) entry. That's our main key in
                # the dictionary.
                self.main_entry_key = entry_value

                # We create the dictionary key.
                self.entries[self.main_entry_key] = {}
                self.entries[self.main_entry_key][self.current_entry_key] = []

            # Python issues... initialization of dictionaries...
            if self.current_entry_key not in self.entries[self.main_entry_key]:
                self.entries[self.main_entry_key][self.current_entry_key] = []

            # Append the value in the correct dictionary keys.
            self.entries[self.main_entry_key][self.current_entry_key].append(
                entry_value)

        # Means we have a line that doesn't start with an entry mark. In other words, an ordinary line value.
        # It occurs only when we have a entry with more than a single value.
        else:

            # Very important: I made the choice of ignoring the '///' chars that marks a end of a entry in a DBGET file.
            # I did it for two reasons: first, we never know when that kind of help (a specific char sequence that marks an end) will occurs from the database vendor,
            # second, I've completely forgoten that mark exists, so I start coding thinking a new entry starts when the previously
            # one is done, without ending mark.
            # The regex match any sequence that starts with whitespaces OR any
            # sequence that starts with '/' (the end mark is typically a
            # sequence like '///').
            entry_record = re.compile(r'(^\s{1,}(.*)$)|(^\/(.*)$)')
            entry_value = entry_record.search(line)
            entry_value = entry_value.group(1)

            # IMPORTANT: it can be a little bit risky... we're removing all the whitespaces from the beggining of the value. Why risky? Because biological data is crazy and
            # I'm affraid there's a entry value that has a starting whitespace as an important part of the value.
            # But of course, it doesn't make any sense, so we're going to
            # remove it.
            if entry_value is not None:
                entry_value = re.sub('^\s{1,}', '', entry_value)

            # Append the value in the correct dictionary keys.
            if entry_value is not None:
                self.entries[self.main_entry_key][self.current_entry_key].append(
                    entry_value)

        # If we finished an entry reading, we have to put the values nested in
        # its correct entry.
        if self.stop == 1:

            # Python issues... starting dictonaries...
            if self.current_entry_key not in self.entries[self.main_entry_key]:
                self.entries[self.main_entry_key][self.current_entry_key] = []

        # nah.
        return 1
