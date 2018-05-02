Version History
===============
0.3.0
-----
Makes the module usable with DBAPI modules with native cursors by proxying
cursors coming from the connection pool. Adds the option to run some SQL
each time a connection is taken from the pool. Also fixes some long-standing
but recently discovered bugs.

0.2.4
-----
Adds a parameter store which has allowed for some new ways to build queries.
There are now two ways to change the value of a parameter to a statement,
and nested queries within other statements can work for the named, pyformat,
and numeric parameter types. Some bug fixes accompany these changes.

0.2.3
-----
When building a SQL statement, users no longer have to explicitly construct an
instance of a value class to pass in a query parameter. This is handled by
BreezeBlocks when passing a literal to a BreezeBlocks operator or a SQL builder
class. This update also introduces a generic value class, which should be easier
to use than the existing paramstyle-specific ones.

0.2.2
-----
Change the method signature for creating a database, and for executing any
SQL statement. The change to the database initialization arguments is a
breaking change.

0.2.1
-----
Adds DML functionality. New builders and new operations for database inserts,
updates, and deletes have been added. They are accessible from the Database
class just like the query builder.

The new builders use a similar interface to the query builder, and the new
operations use a similar interface to the query.

0.2.0
-----
Divide the responsibilities of building and representing a query between two
classes, Query and the new QueryBuilder.

If upgrading from a previous version, please review the Query and QueryBuilder
classes. When building a query, query_builder.get() must now be invoked to
get a usable query object.

0.1.1
-----
Introduces the Column Collection concept to the code, and starts using its
implementation in tables, joins, and queries.

0.1.0
-----
Query functionality covers enough possibilities of the SQL language to meet
most anticipated developer needs.
