"""A safe value to use in building SQL statements."""
from .expressions import ConstantExpr

class Value(ConstantExpr):
    pass
