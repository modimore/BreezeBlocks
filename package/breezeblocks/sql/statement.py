class Statement(object):
    """Represents a SQL statement which has been built.
    
    Methods on child classes have at least the parameters listed here
    so specifying any of them by name will work, but child classes
    may add more parameters to support statement-specific functionality.
    """
    def __init__(self, db=None):
        """
        :param db: The database to execute this statement against.
        """
        raise NotImplementedError()
        
    def execute(self, conn=None):
        """Executes the prepared statement in the database.
        
        :param conn: Optional connection to use to execute this statement.
            If this is not provided one will be borrowed from the database's pool.
        """
        raise NotImplementedError()
    
    def set_param(self, param_key, value):
        """Sets a bound parameter for the statement.
        
        :param param_key: The identifier of the parameter to set.
        :param value: The value to assign to the parameter.
        """
        raise NotImplementedError()
    
    def show(self):
        """Prints the constructed SQL with placeholders for bound parameters."""
        raise NotImplementedError()