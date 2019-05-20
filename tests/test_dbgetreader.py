import sys
import pprint
import os
import unittest
from dbgetreader.dbgetreader import DBGETReader 
from dbgetreader.dbget import DBGET
import re

class test_DBGETReader( unittest.TestCase):

    def setUp( self ):

        dbget = DBGET(file_to_read='./tests/fixtures/enzyme')
        self.dbgetr = DBGETReader(reader=dbget)

    def test_entries_position( self ):

        positions = self.dbgetr.entries_position() 
        self.assertTrue( type( positions ) is list )
        self.assertTrue( len( positions ) > 1 )

    def test_parsed_entry( self ):

        positions = self.dbgetr.entries_position() 

        for position in positions:
            entry = self.dbgetr.parsed_entry( position )
            break

        if entry['ENTRY'][0] == 'EC 1.1.1.1                  Enzyme':
            ok = True
        else:
            ok = False

        self.assertTrue( ok )

    def test_all_entries( self ):

        entries = self.dbgetr.all_entries()

        self.assertTrue( type( entries ) is list )

        if entries[0]['ENTRY'][0] == 'EC 1.1.1.1                  Enzyme':
            ok = True
        else:
            ok = False

        self.assertTrue( ok )

if __name__ == "__main__":
    unittest.main()
