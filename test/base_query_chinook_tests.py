from breezeblocks import Table
from breezeblocks.exceptions import QueryError
from breezeblocks.sql.aggregates import Count_, RecordCount
from breezeblocks.sql.join import InnerJoin, FullJoin, LeftJoin, RightJoin, CrossJoin
from breezeblocks.sql.operators import Equal_, In_
from breezeblocks.sql import Value


class BaseQueryChinookTests(object):
    """Tests with the Chinook Database"""
    
    tables = {
        "Artist": Table("Artist", ["ArtistId", "Name"]),
        "Genre": Table("Genre", ["GenreId", "Name"]),
        "Album": Table("Album", ["AlbumId", "Title", "ArtistId"]),
        "Track": Table("Track",
            ["TrackId", "Name", "AlbumId", "MediaTypeId", "GenreId", "Composer", "Milliseconds", "Bytes", "UnitPrice"]),
        "Playlist": Table("Playlist", ["PlaylistId", "Name"]),
        "PlaylistTrack": Table("PlaylistTrack", ["PlaylistId", "TrackId"])
    }
    
    def test_tableQuery(self):
        """Tests a simple select on a table."""
        q = self.db.query(self.tables["Artist"]).get()
        
        # Assertion checks that all columns in the table are present in
        # each row returned.
        for row in q.execute():
            self.assertTrue(hasattr(row, "ArtistId"))
            self.assertTrue(hasattr(row, "Name"))
    
    def test_columnQuery(self):
        """Tests a simple select on a column."""
        q = self.db.query(self.tables["Artist"].getColumn("Name")).get()
        
        # Assertion checks that only the queried columns are returned.
        for row in q.execute():
            self.assertTrue(hasattr(row, "Name"))
            self.assertFalse(hasattr(row, "ArtistId"))
    
    def test_simpleWhereClause(self):
        """Tests a simple where clause."""
        tbl_genre = self.tables["Genre"]
        tbl_track = self.tables["Track"]
        genre_id = self.db.query(tbl_genre)\
            .where(tbl_genre.getColumn("Name") == "Alternative & Punk")\
            .get().execute()[0].GenreId
        
        q = self.db.query(tbl_track.getColumn("GenreId"))\
            .where(tbl_track.getColumn("GenreId") == genre_id)\
            .get()
        
        # Assertion checks that the where condition has been applied to
        # the results of the query.
        for track in q.execute():
            self.assertEqual(genre_id, track.GenreId)
    
    def test_nestedQueryInWhereClause(self):
        tbl_album = self.tables["Album"]
        tbl_genre = self.tables["Genre"]
        tbl_track = self.tables["Track"]
        
        genre_id = self.db.query(tbl_genre)\
            .where(tbl_genre.getColumn("Name") == "Alternative & Punk")\
            .get().execute()[0].GenreId
        
        
        track_query = self.db.query(tbl_track.getColumn("AlbumId"))\
            .where(tbl_track.getColumn("GenreId") == genre_id).get()
        
        album_query = self.db.query(tbl_album.getColumn("AlbumId"))\
                .where(
                    In_(
                        tbl_album.getColumn("AlbumId"),
                        self.db.query(tbl_track.getColumn("AlbumId"))\
                            .where(tbl_track.getColumn("GenreId") == genre_id).get()
                    )
                ).get()
        
        albums = album_query.execute()
        tracks = track_query.execute()
        album_ids = set(row.AlbumId for row in tracks)
        self.assertEqual(len(albums), len(album_ids))
        for row in albums:
            self.assertTrue(row.AlbumId in album_ids)
    
    def test_aliasTable(self):
        tbl_album = self.tables["Album"]
        tbl_artist = self.tables["Artist"]
        
        artist_id = self.db.query(tbl_artist.getColumn("ArtistId"))\
            .where(Equal_(tbl_artist.getColumn("Name"), "Queen"))\
            .get().execute()[0].ArtistId
        
        musician = tbl_artist.as_("Musician")
        q = self.db.query(musician).where(Equal_(musician.getColumn("ArtistId"), Value(artist_id))).get()
        
        for row in q.execute():
            self.assertTrue(hasattr(row, "ArtistId"))
            self.assertTrue(hasattr(row, "Name"))
            self.assertEqual(artist_id, row.ArtistId)
    
    def test_selectFromQuery(self):
        tbl_album = self.tables["Album"]
        tbl_artist = self.tables["Artist"]
        
        artist_id = self.db.query(tbl_artist.getColumn("ArtistId"))\
            .where(Equal_(tbl_artist.getColumn("Name"), "Queen"))\
            .get().execute()[0].ArtistId
        
        inner_q = self.db.query(tbl_album.getColumn("ArtistId"), tbl_album.getColumn("Title"))\
            .where(Equal_(tbl_album.getColumn("ArtistId"), Value(artist_id))).get()
        
        q = self.db.query(inner_q.as_("q")).get()
        
        for row in q.execute():
            self.assertTrue(hasattr(row, "ArtistId"))
            self.assertTrue(hasattr(row, "Title"))
            self.assertEqual(artist_id, row.ArtistId)
    
    def test_groupBy(self):
        tbl_track = self.tables["Track"]
        
        q = self.db.query(tbl_track.getColumn("GenreId"), Count_(tbl_track.getColumn("TrackId")).as_("TrackCount"))\
            .group_by(tbl_track.getColumn("GenreId")).get()
        
        for row in q.execute():
            self.assertTrue(hasattr(row, "GenreId"))
            self.assertTrue(hasattr(row, "TrackCount"))
    
    def test_having(self):
        tbl_track = self.tables["Track"]
        
        q = self.db.query(tbl_track.getColumn("GenreId"), Count_(tbl_track.getColumn("TrackId")).as_("TrackCount"))\
            .group_by(tbl_track.getColumn("GenreId"))\
            .having(Count_(tbl_track.getColumn("TrackId")) > 25).get()
        
        for row in q.execute():
            self.assertTrue(hasattr(row, "GenreId"))
            self.assertTrue(hasattr(row, "TrackCount"))
            self.assertLess(25, row.TrackCount,
                "The track count should be greater than specified in the "
                "having clause."
            )
    
    def test_havingMustHaveGroupBy(self):
        tbl_track = self.tables["Track"]
        
        with self.assertRaises(QueryError):
            self.db.query(tbl_track.getColumn("GenreId"), Count_(tbl_track.getColumn("TrackId")).as_("TrackCount"))\
                .having(Count_(tbl_track.getColumn("TrackId")) > 25).get()
    
    def test_orderByAsc(self):
        tbl_artist = self.tables["Artist"]
        
        q = self.db.query(tbl_artist.getColumn("Name"))\
            .order_by(tbl_artist.getColumn("Name")).get()
        
        rows = q.execute()
        prev_name = rows[0].Name
        for row in rows:
            self.assertLessEqual(prev_name, row.Name)
            prev_name = row.Name
    
    def test_orderByDesc(self):
        tbl_artist = self.tables["Artist"]
        
        q = self.db.query(tbl_artist.getColumn("Name"))\
            .order_by(tbl_artist.getColumn("Name"), ascending=False).get()
        
        rows = q.execute()
        prev_name = rows[0].Name
        for row in rows:
            self.assertGreaterEqual(prev_name, row.Name)
            prev_name = row.Name
    
    def test_orderByNullsFirst(self):
        tbl_track = self.tables["Track"]
        
        q = self.db.query(tbl_track.columns["Composer"])\
            .order_by(tbl_track.columns["Composer"], nulls="first")\
            .get()
        
        seen_value = False
        for row in q.execute():
            if not seen_value and row.Composer is not None:
                seen_value = True
            self.assertEqual(row.Composer is not None, seen_value)
    
    def test_orderByNullsLast(self):
        tbl_track = self.tables["Track"]
        
        q = self.db.query(tbl_track.columns["Composer"])\
            .order_by(tbl_track.columns["Composer"], nulls="last")\
            .get()
        
        seen_null = False
        for row in q.execute():
            if not seen_null and row.Composer is None:
                seen_null = True
            self.assertEqual(row.Composer is None, seen_null)
    
    def test_limit(self):
        limit_amount = 5
        
        tbl_track = self.tables["Track"]
        
        q = self.db.query(tbl_track.getColumn("Name")).get()
        
        rows = q.execute(limit=limit_amount)
        self.assertLessEqual(len(rows), limit_amount,
            "Number of rows should not be more than the limit amount.")
    
    def test_limitAndOffset(self):
        limit_amount = 100
        tbl_track = self.tables["Track"]
        
        q0 = self.db.query(tbl_track.getColumn("TrackId"))\
            .order_by(tbl_track.getColumn("TrackId"))\
            .get()
        q1 = self.db.query(tbl_track.getColumn("TrackId"))\
            .order_by(tbl_track.getColumn("TrackId"))\
            .get()
        
        id_set = set(r.TrackId for r in q0.execute(limit=limit_amount))
        
        for row in q1.execute(limit_amount, limit_amount):
            self.assertTrue(row.TrackId not in id_set,
                "Using offset should result in different data being "
                "returned than that of a non-offset query."
            )
    
    def test_distinct(self):
        # Uses album 73 (Eric Clapton Unplugged) because it has multiple genres
        # of track on the album. It just seems a bit less trivial than most
        # albums as a test case.
        album_id = 73
        tbl_track = self.tables["Track"]
        
        q0 = self.db.query(tbl_track.getColumn("GenreId"))\
            .where(tbl_track.getColumn("AlbumId") == album_id).get()
        
        q1 = self.db.query(tbl_track.getColumn("GenreId"))\
            .where(tbl_track.getColumn("AlbumId") == album_id)\
            .distinct().get()
        
        genres0 = set(row.GenreId for row in q0.execute())
        genres1 = [row.GenreId for row in q1.execute()]
        self.assertEqual(len(genres0), len(genres1),
            "Set of all genres in the album should be the same size as "
            "the list of genres retrieved with SELECT DISTINCT."
        )
    
    def test_innerJoin(self):
        tbl_album = self.tables["Album"]
        tbl_track = self.tables["Track"]
        
        tbl_joinAlbumTrack = InnerJoin(tbl_album, tbl_track, using=["AlbumId"])
        
        q = self.db.query(
            tbl_joinAlbumTrack.left,
            tbl_joinAlbumTrack.right.getColumn("Name")).get()
        
        for row in q.execute():
            self.assertEqual(4, len(row))
            self.assertTrue(hasattr(row, "AlbumId"))
            self.assertTrue(hasattr(row, "Title"))
            self.assertTrue(hasattr(row, "ArtistId"))
            self.assertTrue(hasattr(row, "Name"))
    
    def test_leftOuterJoin(self):
        tbl_track = self.tables["Track"]
        tbl_playlist_track = self.tables["PlaylistTrack"]
        
        tbl_leftJoinTrackPlaylistTrack = LeftJoin(tbl_track, tbl_playlist_track, using=["TrackId"])
        
        q = self.db.query(
            tbl_leftJoinTrackPlaylistTrack.left.getColumn("TrackId"),
            tbl_leftJoinTrackPlaylistTrack.right.getColumn("PlaylistId")
        ).get()
        
        num_tracks = len(self.db.query(tbl_track.columns["TrackId"]).distinct().get().execute())
        
        rows = q.execute()
        self.assertGreaterEqual(len(rows), num_tracks)
        for row in rows:
            self.assertTrue(hasattr(row, "TrackId"))
            self.assertNotEqual(row.TrackId, None)
            self.assertTrue(hasattr(row, "PlaylistId"))
    
    def test_rightOuterJoin(self):
        tbl_genre = self.tables["Genre"]
        tbl_track = self.tables["Track"]
        
        tbl_rightJoinTrackGenre = RightJoin(tbl_track, tbl_genre, using=["GenreId"])
        
        q = self.db.query(
            tbl_rightJoinTrackGenre.left.getColumn("TrackId"),
            tbl_rightJoinTrackGenre.right.getColumn("GenreId")
        ).get()
        
        num_genres = len(self.db.query(tbl_genre.columns["GenreId"]).distinct().get().execute())
        
        rows = q.execute()
        self.assertGreaterEqual(len(rows), num_genres)
        for row in rows:
            self.assertTrue(hasattr(row, "TrackId"))
            self.assertTrue(hasattr(row, "GenreId"))
            self.assertNotEqual(row.GenreId, None)
    
    def test_fullOuterJoin(self):
        tbl_genre = self.tables["Genre"]
        tbl_track = self.tables["Track"]
        
        tbl_rightJoinTrackGenre = FullJoin(tbl_track, tbl_genre, using=["GenreId"])
        
        q = self.db.query(
            tbl_rightJoinTrackGenre.left.getColumn("TrackId"),
            tbl_rightJoinTrackGenre.right.getColumn("GenreId")
        ).get()
        
        num_tracks = len(self.db.query(tbl_track.columns["TrackId"]).distinct().get().execute())
        num_genres = len(self.db.query(tbl_track.columns["GenreId"]).distinct().get().execute())
        
        rows = q.execute()
        self.assertGreaterEqual(len(rows), num_tracks)
        self.assertGreaterEqual(len(rows), num_genres)
        for row in rows:
            self.assertTrue(hasattr(row, "TrackId"))
            self.assertTrue(hasattr(row, "GenreId"))
    
    def test_crossJoin(self):
        tbl_playlist = self.tables["Playlist"]
        tbl_track = self.tables["Track"]
        
        playlistRecordCount = self.db.query()\
            .from_(tbl_playlist)\
            .select(RecordCount())\
            .get().execute()[0][0]
        
        trackRecordCount = self.db.query()\
            .from_(tbl_track)\
            .select(RecordCount())\
            .get().execute()[0][0]
        
        q = self.db.query()\
            .from_(CrossJoin(tbl_playlist, tbl_track))\
            .select(RecordCount().as_("RecordCount"))\
            .get()
        
        joinSizeRow = q.execute()[0]
        
        self.assertEqual(playlistRecordCount * trackRecordCount, joinSizeRow.RecordCount,
            "The cross join should contain as many records as "
            "the number of playlists times the number of tracks."
        )
    
    def test_joinOn(self):
        tbl_album = self.tables["Album"]
        tbl_track = self.tables["Track"]
        
        tbl_joinAlbumTrack = InnerJoin(tbl_album, tbl_track,
            on=[Equal_(tbl_album.getColumn("AlbumId"), tbl_track.getColumn("AlbumId"))]
        )
        
        q = self.db.query(
            tbl_joinAlbumTrack.left,
            tbl_joinAlbumTrack.right.getColumn("AlbumId").as_("TrackAlbumId"),
            tbl_joinAlbumTrack.right.getColumn("Name")).get()
        
        for row in q.execute():
            self.assertEqual(5, len(row))
            self.assertTrue(hasattr(row, "AlbumId"))
            self.assertTrue(hasattr(row, "TrackAlbumId"))
            self.assertTrue(hasattr(row, "Title"))
            self.assertTrue(hasattr(row, "ArtistId"))
            self.assertTrue(hasattr(row, "Name"))
            self.assertEqual(row.AlbumId, row.TrackAlbumId)
    
    def test_multipleJoins(self):
        tbl_album = self.tables["Album"]
        tbl_artist = self.tables["Artist"]
        tbl_track = self.tables["Track"]
        
        tbl_joinAlbumTrack = InnerJoin(tbl_album, tbl_track, using=["AlbumId"])
        tbl_joinArtistAlbumTrack = InnerJoin(tbl_artist, tbl_joinAlbumTrack, using=["ArtistId"])
        
        q = self.db.query(
            tbl_joinArtistAlbumTrack.tables["Artist"].getColumn("ArtistId"),
            tbl_joinArtistAlbumTrack.tables["Album"].getColumn("ArtistId").as_("AlbumArtistId"),
            tbl_joinArtistAlbumTrack.tables["Album"].getColumn("AlbumId"),
            tbl_joinArtistAlbumTrack.tables["Track"].getColumn("Name").as_("TrackName")
        ).get()
        
        for row in q.execute():
            self.assertTrue(hasattr(row, "ArtistId"))
            self.assertTrue(hasattr(row, "AlbumArtistId"))
            self.assertTrue(hasattr(row, "AlbumArtistId"))
            self.assertTrue(hasattr(row, "TrackName"))
            self.assertEqual(row.ArtistId, row.AlbumArtistId)
    
    def test_setQueryParamValue(self):
        tbl_genre = self.tables["Genre"]
        tbl_track = self.tables["Track"]
        
        genres = self.db.query(tbl_genre).get().execute(2)
        
        genre1_id = genres[0].GenreId
        genre2_id = genres[1].GenreId
        
        genre_id_param = Value(genre1_id, param_name="genre_id")
        
        q = self.db.query(tbl_track.getColumn("GenreId"))\
            .where(tbl_track.getColumn("GenreId") == genre_id_param)\
            .get()
        
        # Assertion checks that the where condition has been applied to
        # the results of the query.
        for track in q.execute():
            self.assertEqual(genre1_id, track.GenreId)
        
        q.set_param("genre_id", genre2_id)
        
        for track in q.execute():
            self.assertEqual(genre2_id, track.GenreId)
