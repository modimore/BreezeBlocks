from ..exceptions import DeleteError

class Delete(object):
    """Represents a database delete."""
    
    def __init__(self, statement, params, db=None):
        """Initializes a delete statement against a specific database.
        
        :param statement: The SQL statement for the delete.
        :param params: A list of literal values to pass into the statement.
        :param db: The database to perform the delete on.
        """
        if db is None:
            raise DeleteError('Attempting to delete without a database.')
        
        self._db = db
        self._statement = statement
        self._params = params
    
    def execute(self):
        """Executes the delete in the database."""
        with self._db.pool.get() as conn:
            cur = conn.cursor()
            cur.execute(self._statement, self._params)
            cur.close()
            conn.commit()
    
    def show(self):
        """Show the constructed SQL statement for this delete."""
        print(self._statement, self._params, sep='\n')
