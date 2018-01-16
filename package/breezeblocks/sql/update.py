from ..exceptions import UpdateError

class Update(object):
    """Represents a database update."""
    
    def __init__(self, statement, params, db=None):
        """Initializes an update statement against a specific database.
        
        :param statement: The SQL statement for the update.
        :param table: The table to update.
        :param columns: The columns in the table being updated.
        :param exprs: The expression the columns are being set to.
        :param db: The database to perform the update on.
        """
        if db is None:
            raise UpdateError('Attempting to update without a database.')
        
        self._db = db
        self._statement = statement
        self._params = params
    
    def execute(self):
        """Executes the update in the database."""
        with self._db.pool.get() as conn:
            cur = conn.cursor()
            cur.execute(self._statement, self._params)
            results = cur.fetchall()
            cur.close()
            conn.commit()
    
    def show(self):
        """Show the constructed SQL statement for this update."""
        print(self._statement, self._params, sep='\n')
