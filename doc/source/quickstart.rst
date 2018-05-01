Quick Start
===========

BreezeBlocks does not require overly much setup. First step is setting the
code up to access your database. Here we'll assume we have an SQLite database
file in the current folder called "Library.sqlite" with a few tables.

.. code-block:: python
   
   import sqlite3
   from breezeblocks import Database
   from breezeblocks.sql import Table
   
   db = Database(dsn="Library.sqlite", dbapi_module=sqlite3)
   authors = Table("Author", ["id", "name"])
   genres = Table("Genre", ["id", "name"])
   books = Table("Book", ["id", "author_id", "genre_id", "title"])

This information here is sufficient to start working with our database,
so let's go ahead and write a simple queries just to test the package out.

.. code-block:: python
   
   get_all_authors = db.query(authors).get()
   get_all_genre_names = db.query(genres.columns["name"]).get()
   get_all_book_titles_and_ids = db.query(
       books.columns["id"], books.columns["title"]).get()

Looks good, now we should try to execute those.

.. code-block:: python
   
   for author in get_all_authors.execute():
       print(author.id, author.name)
   for genre in get_all_genre_names.execute():
       print(genre.name)
   for book in get_all_book_titles_and_ids.execute():
       print(book.id, book.title)

The book and genre queries gave us everything we asked for and the
author query gave us all the columns of `Author`, so now we know we can
write and execute a basic query.

DML statements are built out similarly to queries in BreezeBlocks. For example,
we can insert records like this. As you might have noticed when querying all
books, we have just the first six Harry Potter books in the library. Kids
seem to love those, so let's get some more in there.

.. code-block:: python
   
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

We could only get our hands on three more for now, but that's a good start.
Looks like whoever was cataloging these didn't spell "Deathly" right. Easy
mistake. Let's fix that one.

.. code-block:: python
   
   update_deadly_hallows = db.update(books)\
       .set(books.columns["title"], "Harry Potter and the Deathly Hallows")\
       .where(books.columns["title"] == "Harry Potter and the Deadly Hallows")\
       .get()
   update_deadly_hallows.execute()

Let's take a look at the books we have in the database now. You can just
execute the `book_titles_and_ids` query again to do so. It looks pretty
comprehensive for the main series. "Sorceror's Stone" and "Philospher's Stone"
are the same book, so we can probably remove one of their entries. They
can be categorized as the same thing as far as the library is concerned. We'll
just delete one of those entries then.

.. code-block:: python
   
   delete_sorcerors_stone = db.delete(books)\
       .where(
           books.columns["title"] == "Harry Potter and the Sorceror's Stone"
       ).get()
   delete_sorcerors_stone.execute()

Now you've seen the basic functionality and how to use it, you can check out
the API reference to see what else you can do with the package.
