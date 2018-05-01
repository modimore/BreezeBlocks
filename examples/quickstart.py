import sqlite3
from breezeblocks import Database
from breezeblocks.sql import Table

# Setup
db = Database(dsn="Library.sqlite", dbapi_module=sqlite3)
authors = Table("Author", ["id", "name"])
genres = Table("Genre", ["id", "name"])
books = Table("Book", ["id", "author_id", "genre_id", "title"])

# Query
get_all_authors = db.query(authors).get()
get_all_genre_names = db.query(genres.columns["name"]).get()
get_all_book_titles_and_ids = db.query(
    books.columns["id"], books.columns["title"]).get()

for author in get_all_authors.execute():
    print(author.id, author.name)
for genre in get_all_genre_names.execute():
    print(genre.name)
for book in get_all_book_titles_and_ids.execute():
    print(book.id, book.title)

# Insert
insert_books = db.insert(books).add_columns(
    "author_id", "genre_id", "title").get()

jkr_query = db.query(authors.columns["id"])\
    .where(authors.columns["name"] == "J.K. Rowling").get()
jkr_id = jkr_query.execute()[0].id
fantasy_query = db.query(genres.columns["id"])\
    .where(genres.columns["name"] == "Fantasy").get()
fantasy_id = fantasy_query.execute()[0].id

insert_books.execute([
 (jkr_id, fantasy_id, "Harry Potter and the Deadly Hallows"),
 (jkr_id, fantasy_id, "Harry Potter and the Sorceror's Stone")
])

# Update
update_deadly_hallows = db.update(books)\
    .set_(books.columns["title"], "Harry Potter and the Deathly Hallows")\
    .where(books.columns["title"] == "Harry Potter and the Deadly Hallows")\
    .get()
update_deadly_hallows.execute()

# Delete
delete_sorcerors_stone = db.delete(books)\
    .where(
        books.columns["title"] == "Harry Potter and the Sorceror's Stone"
    ).get()
delete_sorcerors_stone.execute()
