from .exceptions import InsertError
from .sql.insert import Insert

class InsertBuilder(object):
    def __init__(self, table, columns=[], db=None):
        if db is None:
            raise InsertError('Attempting to build an insert statement without a database.')
        
        self._db = db
        self._table = table
        self._column_names = []
        self.add_columns(*columns)
    
    def add_columns(self, *columns):
        """Adds all columns in the arguments to the insert statement.
        
        :param columns: All arguments provided to the method.
          Column names as strings and `Column` objects are accepted.
        
        :return: `self` for method chaining.
        """
        for column in columns:
            if isinstance(column, str):
                column_name = column
            else:
                column_name = column.name
            
            self._table.columns[column_name] # Should raise exception if no column with name exists in table
            self._column_names.append(column_name)
        
        return self
    
    def get(self):
        return Insert(self._construct_sql(), self._table, self._column_names, db=self._db)
    
    def _construct_sql(self):
        return 'INSERT INTO {0} ({1})'.format(
            self._table.name,
            ','.join(self._column_names)
        )
