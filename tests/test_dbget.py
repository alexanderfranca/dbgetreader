import sys
import pprint
import os
import unittest
from dbgetreader.dbget import DBGET 
import re


class TestDBGET( unittest.TestCase):

    def setUp( self ):

        self.dbget = DBGET('./tests/fixtures/enzyme')

    def test_is_end_of_entry( self ):

        string = '///'

        self.assertTrue( self.dbget.is_end_of_entry( string ) )

    def test_entries_position( self ):

        self.dbget.generate_entries_position()

        self.assertTrue( type( self.dbget.entries_position ) is list )
        self.assertTrue( len( self.dbget.entries_position ) > 1 )

    def test_generate_entries_position( self ):

        self.dbget.generate_entries_position()

        self.assertTrue( type( self.dbget.entries_position ) is list )
        self.assertTrue( len( self.dbget.entries_position ) > 1 )


    def test_entry_data( self ):

        entries = self.dbget.whole_file_data()

        self.assertTrue( type( entries ) is dict )

        # Why an if? Because it's horrible to read this entire entry string in a test.
        if 'ec00071  Fatty acid degradation' in entries['EC 1.1.1.1                  Enzyme']['PATHWAY']:
            ok = True
        else:
            ok = False

        self.assertTrue( ok )

if __name__ == "__main__":
    unittest.main()
