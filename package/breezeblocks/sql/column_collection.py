"""Classes that represent a collection of columns.

It is convenient to be able to reference a collection of columns that are a
subset of what is in a table, or from one of the tables in a join, or in any
other scenario where the columns referenced are not part of a collection
implied by another class.
"""

from ..exceptions import MissingColumnError

class ColumnCollection(object):
    """Represents a collection of columns in a database.
    
    Instances are meant to be passed to the `select` method of `Query` objects.
    Calling `select` on one of these adds all of the columns in it to the
    select clause of the query.
    """
    
    def __init__(self, columns):
        self._column_names = tuple(column._get_name() for column in columns)
        self._columns = {column._get_name(): column for column in columns}
    
    def _get_selectables(self):
        return [self._columns[name] for name in self._column_names]
    
    def _get_tables(self):
        tables = set()
        for column in self._columns.values():
            tables.update(column._get_tables())
        return tables
    
    def _get_column(self, key):
        if not isinstance(key, str):
            raise TypeError("Column Collections require strings for column names.")
        
        try:
            return self._columns[key]
        except KeyError:
            raise MissingColumnError(key)
    
    def __contains__(self, key):
        return key in self._columns
    
    def __getitem__(self, key):
        try:
            return self._get_column(key)
        except MissingColumnError:
            raise KeyError
    
    def get_column(self, key):
        """:return: The specified column from the collection."""
        return self._get_column(key)
    
    def get_names(self):
        """:return: The names of all columns in the collection."""
        return self._column_names
