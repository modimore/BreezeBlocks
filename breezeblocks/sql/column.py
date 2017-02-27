"""Provides a column class and an expression for using columns in queries."""
from .expressions import _Expr

class _BaseColumnExpr(_Expr):
    """A class that marks subclasses as representing database columns.
    
    This should means it is safe to construct column expressions
    from them, and will allow a :class:`Query` to do so.
    """
    def __init__(object):
        raise NotImplementedError()

class ColumnExpr(_BaseColumnExpr):
    """Represents a database column."""
    def __init__(self, name, table):
        """Initializes a column.
        
        :param name: The name of this column.
        
        :param table: The table to which this column belongs.
        """
        self.name = name
        
        self.table = table
        self.full_name = '.'.join([table.name, self.name])
    
    def ref_field(self):
        """Returns a way to reference this column in a query."""
        return self.full_name
    
    def select_field(self):
        """Returns the expression for selecting this column in a
        query."""
        return '{} AS {}'.format(
            self.full_name, self.name)
    
    def as_(self, alias):
        """Provides a different alias for the same underlying column.
        
        :param alias: Another alias to use.
        """
        return AliasedColumnExpr(alias, self)

class AliasedColumnExpr(_BaseColumnExpr):
    """A column with an alias used in querying."""
    def __init__(self, alias, column):
        """Initializes an aliased column from an existing column.
        
        :param alias: The alias that will be assigned to this object.
        
        :param column: The :class:`Column` that this is going to reference.
        """
        self.column = column
        self.name = alias
    
    @property
    def table(self):
        """Returns the table of the underlying column."""
        return self.column.table
    
    @property
    def full_name(self):
        """Returns the full name of the underlying column."""
        return self.column.full_name
    
    def ref_field(self):
        """Returns a way to reference this column in a query."""
        return self.full_name
    
    def select_field(self):
        """Returns the expression for selecting this column in a
        query."""
        return '{} AS {}'.format(
            self.full_name, self.name)
    
    def as_(self, alias):
        """Provides a different alias for the same underlying column.
        
        :param alias: Another alias to use.
        """
        return AliasedColumnExpr(alias, self.column)
