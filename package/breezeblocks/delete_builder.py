from io import StringIO

from .exceptions import DeleteError
from .sql.delete import Delete

class DeleteBuilder(object):
    def __init__(self, table, db=None):
        if db is None:
            raise DeleteError('Attemping to build a delete statement without a database.')
        
        self._db = db
        self._table = table
        self._conditions = []
    
    def get(self):
        statement, params = self._construct_sql()
        return Delete(statement, params, self._db)
    
    def where(self, *conditions):
        """Adds filtering conditions to the rows to delete.
        
        :param conditions: The expression to filter with.
        
        :return: `self` for method chaining.
        """
        self._conditions.extend(conditions)
        
        return self
    
    def _construct_sql(self):
        statement_buffer = StringIO()
        params = []
        
        statement_buffer.write('DELETE FROM {}'.format(self._table.name))
        
        if len(self._conditions) > 0:
            statement_buffer.write('\nWHERE ')
            
            statement_buffer.write('\n  AND '.join(
                cond._get_ref_field() for cond in self._conditions))
            for cond in self._conditions:
                params.extend(cond._get_params())
        
        return (statement_buffer.getvalue(), params)
