# Contributing

If you feel that you understand this project well enough, just read through
this top section and then proceed to contribute what you will.

* On code-style related issues, refer to [PEP8][]
  * Prefer double quotes to single quotes. PEP8 takes no stance on this.
* Open a pull request to merge into master when you're ready.
  * Part of readiness should be the ability to fill out the relevant sections
    of the template.

[pep8]: https://www.python.org/dev/peps/pep-0008/

## Project Overview & Goals

BreezeBlocks is a SQL statement builder designed for people attempting to
use a database from the Python programming language. The target audience has
at least a working knowledge of SQL and wants a solution that can be used to
build SQL statements, execute them, and retrieve their results if applicable.
BreezeBlocks does this by providing a builder interface for various types of
statements, allowing users to progressively construct what they need, then get
a finalized executable (has an `execute` method) object that can be used to
perform the built action.

SQL should be in the spotlight in this package. Connections, cursors, and other
details are for the most part handled by the BreezeBlocks and not the end-user.

## Useful things to know

There are only a few key skills that are prominently used when working on most
of this project. When working on the core components of the project, these
are going to be the most important areas of knowledge:

* Python
* SQL
* The Builder Pattern

These are secondary or handle implementation details that are either going to
relate mostly to internal implementation details, or are just expected to
be an overall much smaller part of the code written to use BreezeBlocks.

* Dependency Injection
* Object Pooling

## Open Tasks

General improvements to the code itself are certainly welcome, but some of
these items are perhaps more pressing.

###### Unit tests

There are only tests for SQLite right now, but it's desirable to have formal
tests with other RDBMSes and SQL dialects. This shouldn't mean to test N
RDBMSes there should be N indepenent test classes. Passing a different DBAPI
module when constructing the `breezeblocks.Database` object should hopefully
allow re-use of much of the test code, and small bits can be replaced where
one system does not work the same way as most of the others do. The current
tests are using the Chinook database, which should make it a little easier
to facilitate this.

###### Documentation and Examples

Part of the documentation is written on it's own but most of it comes from
docstrings in the code. The most useful addition to the documentation that
exists currently is probably examples of how to use the package, perhaps a
sort of walkthrough of a simple usage scenario.

###### Benchmarks and Profiling

Being faster than everything else isn't crucial to the goals of this project.
For one thing, time spent in the database should be noticeably longer than
time spent in Python, and that can't really be optimized away on this end.
That doesn't make speed and memory footprint a non-concern though, especially
for potential bulk processing. Having a way to test how this project does on
those fronts will come in handy at some point.
