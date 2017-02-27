"""Defines object reprentations for SQL Operators."""
from .abc import Queryable

class _OperatorExpr(object):
    """SQL operator base class that implements common methods."""
    def __init__(self):
        raise NotImplementedError()
    
    def _get_ref_field(self):
        raise NotImplementedError()
    
    def _get_select_field(self):
        return self.as_('_')._get_select_field()
    
    def _get_params(self):
        raise NotImplementedError()
    
    def _get_tables(self):
        raise NotImplementedError()
    
    def as_(self, alias):
        return _AliasedOperatorExpr(self, alias)
    
    # Comparisons
    def __eq__(self, other):
        return Equal_(self, other)
    
    def __ne__(self, other):
        return NotEqual_(self, other)
    
    def __lt__(self, other):
        return LessThan_(self, other)
    
    def __gt__(self, other):
        return GreaterThan_(self, other)
    
    def __le__(self, other):
        return LessThanEqual_(self, other)
    
    def __ge__(self, other):
        return GreaterThanEqual_(self, other)
    
    # Binary Arithmetic operators
    def __add__(self, other):
        return Plus_(self, other)
    
    def __sub__(self, other):
        return Minus_(self, other)
    
    def __mul__(self, other):
        return Mult_(self, other)
    
    def __truediv__(self, other):
        return Div_(self, other)
    
    def __mod__(self, other):
        return Mod_(self, other)
    
    def __pow__(self, other):
        return Exp_(self, other)
    
    # Unary Arithmetic operators
    def __pos__(self):
        return UnaryPlus_(self)
    
    def __neg__(self):
        return UnaryMinus_(self)

class _AliasedOperatorExpr(object):
    def __init__(self, operator, alias):
        self._operator = operator
        self._alias = alias
    
    def _get_ref_field(self):
        return '{}'.format(self._operator._get_ref_field())
    
    def _get_select_field(self):
        return '{} AS {}'.format(
            self._operator._get_ref_field(), self._alias)
    
    def _get_tables(self):
        return self._operator._get_tables()

class _UnaryOperator(_OperatorExpr):
    """SQL Unary Operator"""
    def __init__(self, operand):
        self._operand = operand
    
    def _get_params(self):
        return self._operand._get_params()
    
    def _get_tables(self):
        return self._operand._get_tables()

class _BinaryOperator(_OperatorExpr):
    """SQL Binary Operator"""
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs
    
    def _get_params(self):
        result = []
        result.extend(self._lhs._get_params())
        result.extend(self._rhs._get_params())
        return tuple(result)
    
    def _get_tables(self):
        result = set()
        result.update(self._lhs._get_tables(), self._rhs._get_tables())
        return result

class _ChainableOperator(_OperatorExpr):
    """SQL chainable operator.
    
    This can be used to implement operators that are both
    associative and commutative.
    See `Or_`, `And_`, or `Plus_` as an example."""
    def __init__(self, *operands):
        self._operands = operands
    
    def _get_params(self):
        result = []
        for operand in self._operands:
            result.extend(operand._get_params())
        return result
    
    def _get_tables(self):
        result = set()
        result.update(*[o._get_tables() for o in self._operands])

class Or_(_ChainableOperator):
    """SQL 'OR' operator"""
    def _get_ref_field(self):
        return ' OR '.join(
            ['({})'.format(expr._get_ref_field()) for expr in self._operands])

class And_(_ChainableOperator):
    """SQL 'AND' operator"""
    def _get_ref_field(self):
        return ' AND '.join(
            ['({})'.format(expr._get_ref_field()) for expr in self._operands])

class Not_(_UnaryOperator):
    """SQL 'NOT' operator"""
    def _get_ref_field(self):
        return 'NOT ({})'.format(self._operand._get_ref_field())

class Is_(_BinaryOperator):
    """SQL 'IS' operator"""
    def _get_ref_field(self):
        return '({}) IS ({})'.format(
			self._lhs._get_ref_field(), self._rhs._get_ref_field())

class IsNull_(_UnaryOperator):
    """SQL 'IS NULL' operator"""
    def _get_ref_field(self):
        return '({} IS NULL)'.format(self._operand._get_ref_field())

class NotNull_(_UnaryOperator):
    """SQL 'IS NOT NULL' operator"""
    def _get_ref_field(self):
        return '({}) IS NOT NULL'.format(self._operand._get_ref_field())

class Equal_(_BinaryOperator):
    """SQL '=' operator"""
    def _get_ref_field(self):
        return '({}) = ({})'.format(
			self._lhs._get_ref_field(), self._rhs._get_ref_field())

class NotEqual_(_BinaryOperator):
    """SQL '!=' or '<>' operator"""
    def _get_ref_field(self):
        return '({}) <> ({})'.format(
			self._lhs._get_ref_field(), self._rhs._get_ref_field())

class LessThan_(_BinaryOperator):
    """SQL '<' operator"""
    def _get_ref_field(self):
        return '({}) < ({})'.format(
			self._lhs._get_ref_field(), self._rhs._get_ref_field())

class GreaterThan_(_BinaryOperator):
    """SQL '>' operator"""
    def _get_ref_field(self):
        return '({}) > ({})'.format(
			self._lhs._get_ref_field(), self._rhs._get_ref_field())

class LessThanEqual_(_BinaryOperator):
    """SQL '<=' operator"""
    def _get_ref_field(self):
        return '({}) <= ({})'.format(
			self._lhs._get_ref_field(), self._rhs._get_ref_field())

class GreaterThanEqual_(_BinaryOperator):
    """SQL '>=' operator"""
    def _get_ref_field(self):
        return '({}) >= ({})'.format(
			self._lhs._get_ref_field(), self._rhs._get_ref_field())

# BETWEEN IN LIKE ILIKE SIMILAR

# (any other operator)

class Plus_(_ChainableOperator):
    """SQL '+' operator"""
    def _get_ref_field(self):
        return ' + '.join(
            ['({})'.format(expr._get_ref_field()) for expr in self._operands])

class Minus_(_BinaryOperator):
    """SQL '-' operator"""
    def _get_ref_field(self):
        return '({}) - ({})'.format(
			self._lhs._get_ref_field(), self._rhs._get_ref_field())

class Mult_(_ChainableOperator):
    """SQL '*' operator"""
    def _get_ref_field(self):
        return ' * '.join(
            ['({})'.format(expr._get_ref_field()) for expr in self._operands])

class Div_(_BinaryOperator):
    """SQL '/' operator"""
    def _get_ref_field(self):
        return '({}) / ({})'.format(
			self._lhs._get_ref_field(), self._rhs._get_ref_field())

class Mod_(_BinaryOperator):
    """SQL '%' operator"""
    def _get_ref_field(self):
        return '({}) % ({})'.format(
			self._lhs._get_ref_field(), self._rhs._get_ref_field())

class Exp_(_BinaryOperator):
    """SQL '^' operator"""
    def _get_ref_field(self):
        return '({}) ^ ({})'.format(
			self._lhs._get_ref_field(), self._rhs._get_ref_field())

class UnaryPlus_(_UnaryOperator):
    """SQL Unary '+' operator"""
    def _get_ref_field(self):
        return '+({})'.format(self._operand._get_ref_field())

class UnaryMinus_(_UnaryOperator):
    """SQL Unary '-' operator"""
    def _get_ref_field(self):
        return '-({})'.format(self._operand._get_ref_field())

Queryable.register(_OperatorExpr)
Queryable.register(_AliasedOperatorExpr)
