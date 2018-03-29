from breezeblocks import Table
from breezeblocks.sql.operators import Equal_, Like_, Or_
from breezeblocks.sql import Value

class BaseDMLChinookTests(object):
    """DML tests using SQLite with the Chinook Database"""
    
    tables = {
        'Artist': Table('Artist', ['ArtistId', 'Name']),
        'Genre': Table('Genre', ['GenreId', 'Name']),
        'Album': Table('Album', ['AlbumId', 'Title', 'ArtistId']),
        'Track': Table('Track',
            ['TrackId', 'Name', 'AlbumId', 'MediaTypeId', 'GenreId', 'Composer', 'Milliseconds', 'Bytes', 'UnitPrice']),
        'Playlist': Table('Playlist', ['PlaylistId', 'Name']),
        'PlaylistTrack': Table('PlaylistTrack', ['PlaylistId', 'TrackId'])
    }
    
    def test_insertIntoValues(self):
        conn = self.db.pool.get()
        
        i = self.db.insert(self.tables['Artist']).add_columns('Name').get()
        
        i.execute([
            ('Weezer',)
        ], conn=conn)
        
        q = self.db.query(self.tables['Artist'].columns['Name'])\
            .where(Equal_(self.tables['Artist'].columns['Name'], 'Weezer'))\
            .get()
        
        rows = q.execute(conn=conn)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].Name, 'Weezer')
    
    def test_insertIntoSelect(self):
        t_genre = self.tables['Genre']
        t_track = self.tables['Track']
        t_playlist = self.tables['Playlist']
        t_playlistTrack = self.tables['PlaylistTrack']
        
        conn = self.db.pool.get()
        
        genre_id = self.db.query(t_genre.columns['GenreId'])\
            .where(t_genre.columns['Name'] == 'Jazz')\
            .get().execute(limit=1)[0].GenreId
        
        # Setting up the initial playlist row
        self.db.insert(t_playlist).add_columns(t_playlist.columns['Name'])\
            .get().execute([('LP Jazz Mix',)], conn=conn)
        playlist_id = self.db.query(t_playlist.columns['PlaylistId'])\
            .where(t_playlist.columns['Name'] == 'LP Jazz Mix')\
            .get().execute(conn=conn)[0].PlaylistId
        
        # Testing the INSERT INTO SELECT
        i = self.db.insert(t_playlistTrack).add_columns('PlaylistId', 'TrackId')\
            .get()
        q = self.db.query(Value(playlist_id), t_track.columns['TrackId'])\
            .where(t_track.columns['GenreId'] == genre_id).get()
        
        i.execute(q, conn=conn)
        
        q2 = self.db.query(t_playlistTrack.columns['TrackId'])\
            .where(t_playlistTrack.columns['PlaylistId'] == Value(playlist_id))\
            .get()
        
        self.assertEqual(len(q2.execute(conn=conn)), len(q.execute(conn=conn)))
    
    def test_update(self):
        t_genre = self.tables['Genre']
        t_album = self.tables['Album']
        t_track = self.tables['Track']
        
        genre_id = self.db.query(t_genre.columns['GenreId'])\
            .where(Equal_(t_genre.columns['Name'], 'Pop'))\
            .get().execute(limit=1)[0].GenreId
        album_id = self.db.query(t_album.columns['AlbumId'])\
            .where(Equal_(t_album.columns['Title'], 'American Idiot'))\
            .get().execute()[0].AlbumId
        conn = self.db.pool.get()
        
        # This album was recorded in their Pop period
        u = self.db.update(t_track)\
            .set_(t_track.columns['GenreId'], genre_id)\
            .where(Equal_(t_track.columns['AlbumId'], album_id)).get()
        
        u.execute(conn=conn)
        
        q = self.db.query(t_track.columns['GenreId'])\
            .where(Equal_(t_track.columns['AlbumId'], album_id)).get()
        
        for row in q.execute(conn=conn):
            self.assertEqual(row.GenreId, genre_id)
    
    def test_delete(self):
        conn = self.db.pool.get()
        
        # My episodes of Lost are just taking up too much space on my HDD
        d = self.db.delete(self.tables['Album']).where(
            Like_(self.tables['Album'].columns['Title'], 'Lost, Season%')
        ).get()
        
        d.execute(conn)
        
        q = self.db.query(self.tables['Album'].columns['AlbumId']).where(
            Like_(self.tables['Album'].columns['Title'], 'Lost, Season%')
        ).get()
        
        rows = q.execute(conn=conn)
        # All corresponding rows should have been deleted on this connection
        self.assertEqual(len(rows), 0)
    
    def test_setUpdateParamValue(self):
        t_genre = self.tables['Genre']
        t_album = self.tables['Album']
        t_artist = self.tables['Artist']
        t_track = self.tables['Track']
        
        artist_id = self.db.query(t_artist.columns['ArtistId'])\
            .where(Equal_(t_artist.columns['Name'], 'The Clash'))\
            .get().execute()[0].ArtistId
        genres = self.db.query(t_genre.columns['GenreId'])\
            .where(Or_(
                t_genre.columns['Name'] == 'Rock',
                t_genre.columns['Name'] == 'Alternative & Punk'
            )).get().execute()
        album_id = self.db.query(t_album.columns['AlbumId'])\
            .where(Equal_(t_album.columns['ArtistId'], artist_id))\
            .get().execute()[0].AlbumId
        conn = self.db.pool.get()
        
        q = self.db.query(t_track.columns['GenreId'])\
            .where(Equal_(t_track.columns['AlbumId'], album_id)).get()
        
        genre_id_param = Value(genres[0].GenreId, param_name="genre_id")
        
        # Are the Clash Rock or Alternative & Punk?
        u = self.db.update(t_track)\
            .set_(t_track.columns['GenreId'], genre_id_param)\
            .where(Equal_(t_track.columns['AlbumId'], album_id)).get()
        u.execute(conn=conn)
        
        for row in q.execute(conn=conn):
            self.assertEqual(row.GenreId, genres[0].GenreId)
        
        u.set_param("genre_id", genres[1].GenreId)
        u.execute(conn=conn)
        
        for row in q.execute(conn=conn):
            self.assertEqual(row.GenreId, genres[1].GenreId)
    
    def test_setDeleteParamValue(self):
        t_genre = self.tables['Genre']
        t_track = self.tables['Track']
        
        conn = self.db.pool.get()
        
        # Deleting all my CLassical and Opera
        
        genres = self.db.query(t_genre.columns['GenreId'])\
            .where(Or_(
                t_genre.columns['Name'] == 'Classical',
                t_genre.columns['Name'] == 'Opera'
            )).get().execute()
        
        genre_delete_param = Value(genres[0].GenreId, param_name="genre_id")
        
        d = self.db.delete(t_track)\
            .where(t_track.columns['GenreId'] == genre_delete_param).get()
        d.execute(conn=conn)
        
        genre_query_param = Value(genres[0].GenreId, param_name="genre_id")
        q = self.db.query(t_track.columns['TrackId'])\
            .where(t_track.columns['GenreId'] == genre_query_param).get()
        self.assertEqual(len(q.execute(conn=conn)), 0)
        
        d.set_param("genre_id", genres[1].GenreId)
        d.execute(conn=conn)
        
        q.set_param("genre_id", genres[1].GenreId)
        self.assertEqual(len(q.execute(conn=conn)), 0)
