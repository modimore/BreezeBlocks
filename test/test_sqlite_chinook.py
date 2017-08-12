import unittest
import sqlite3
from breezeblocks import Database, Table
from breezeblocks.sql.operators import In_
from breezeblocks.sql.values import QmarkStyleValue as Value

class SQLiteChinookTests(unittest.TestCase):
    """Tests using SQLite with the Chinook Database"""
    
    def setUp(self):
        """Performs necessary SQLite3 setup."""
        self.db = Database('Chinook.sqlite', sqlite3)
        self.tables = {
            'Artist': Table('Artist', ['ArtistId', 'Name']),
            'Genre': Table('Genre', ['GenreId', 'Name']),
            'Album': Table('Album', ['AlbumId', 'Title', 'ArtistId']),
            'Track': Table('Track',
                ['TrackId', 'Name', 'AlbumId', 'MediaTypeId', 'GenreId', 'Composer', 'Milliseconds', 'Bytes', 'UnitPrice'])
        }
    
    def test_tableQuery(self):
        """Tests a simple select on a table."""
        q = self.db.query(self.tables['Artist'])
        
        # Assertion checks that all columns in the table are present in
        # each row returned.
        for row in q.execute():
            self.assertTrue(hasattr(row, 'ArtistId'))
            self.assertTrue(hasattr(row, 'Name'))
    
    def test_columnQuery(self):
        """Tests a simple select on a column."""
        q = self.db.query(self.tables['Artist']['Name'])
        
        # Assertion checks that only the queried columns are returned.
        for row in q.execute():
            self.assertTrue(hasattr(row, 'Name'))
            self.assertFalse(hasattr(row, 'ArtistId'))
    
    def test_simpleWhereClause(self):
        """Tests a simple where clause."""
        tbl_genre = self.tables['Genre']
        tbl_track = self.tables['Track']
        genre_id = self.db.query(tbl_genre)\
            .where(tbl_genre['Name'] == Value('Alternative & Punk'))\
            .execute()[0].GenreId
        
        q = self.db.query(tbl_track['GenreId'])\
                .where(tbl_track['GenreId'] == Value(genre_id))
        
        # Assertion checks that the where condition has been applied to
        # the results of the query.
        for track in q.execute():
            self.assertEqual(track.GenreId, genre_id)
    
    def test_nestedQueryInWhereClause(self):
        tbl_album = self.tables['Album']
        tbl_genre = self.tables['Genre']
        tbl_track = self.tables['Track']
        
        genre_id = self.db.query(tbl_genre)\
            .where(tbl_genre['Name'] == Value('Alternative & Punk'))\
            .execute()[0].GenreId
        
        q = self.db.query(tbl_album['Title'])\
                .where(
                    In_(
                        tbl_album['AlbumId'],
                        self.db.query(tbl_track['AlbumId'])\
                            .where(tbl_track['GenreId'] == Value(genre_id))
                    )
                )
        
        # No assertion here because subqueries because subqueries in the select
        # clause have not been implemented.
        # However, the query running without error is important to test.
        q.execute()
    
