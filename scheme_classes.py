import builtins
from pair import *

class SchemeError(Exception):
    """Exception indicating an error in a Scheme program."""

################
# Environments #
################

class Frame:
    """An environment frame binds Scheme symbols to Scheme values."""

    "*** YOUR CODE HERE ***"
    def __init__(self, parent):
        """An empty frame with parent frame PARENT (which may be None)."""
        self.bindings = {}
        self.parent = parent

    def __repr__(self):
        if self.parent is None:
            return '<Global Frame>'
        s = sorted(['{0}: {1}'.format(k, v) for k, v in self.bindings.items()])
        return '<{{{0}}} -> {1}>'.format(', '.join(s), repr(self.parent))

    def define(self, symbol, value):
        """Define Scheme SYMBOL to have VALUE."""
        # BEGIN PROBLEM 1
        self.bindings.update({symbol: value})
        # END PROBLEM 1

    def lookup(self, symbol):
        """Return the value bound to SYMBOL. Errors if SYMBOL is not found."""
        # Author: Joshua Wong
        # BEGIN PROBLEM 1
        value = self.bindings.get(symbol)
        if value is not None:
            return value
        elif self.parent is not None:
            return self.parent.lookup(symbol)
        # END PROBLEM 1
        raise SchemeError('unknown identifier: {0}'.format(symbol))


    def make_child_frame(self, formals, vals):
        """Return a new local frame whose parent is SELF, in which the symbols
        in a Scheme list of formal parameters FORMALS are bound to the Scheme
        values in the Scheme list VALS. Both FORMALS and VALS are represented
        as Pairs. Raise an error if too many or too few vals are given.

        >>> env = create_global_frame()
        >>> formals, expressions = read_line('(a b c)'), read_line('(1 2 3)')
        >>> env.make_child_frame(formals, expressions)
        <{a: 1, b: 2, c: 3} -> <Global Frame>>
        """
        if len(formals) != len(vals):
            raise SchemeError('Incorrect number of arguments to function call')
        # BEGIN PROBLEM 8
        """ Author: Arshmeet Kaur 
        formals are the parameters, specified in the function definition/signature.
        vals are the arguments, specified when the user puts in the function. 
        The role of this function is to create a new child frame when a function is called and add the bindings."""

        # new frame with parent == self
        child_frame = Frame(self)

        # extract the parameters and arguments
        parameters = []
        arguments = []

        # dump the parameters into a list.
        # handle case where there are no formal parameters
        # if nothing is being bound to anything else, no need to fill parameters or arguments
        if len(formals) == 0:
            pass # both lists stay empty
        else:
            while (True):
                parameters.append(formals.first)
                if formals.rest is nil:
                    break
                formals = formals.rest

            while(True):
                arguments.append(vals.first)
                if vals.rest is nil:
                    break
                vals = vals.rest

            # use to add symbol and value
            for parameter, argument in zip(parameters, arguments):
                # bind parameters to arguments
                child_frame.define(parameter, argument)

        return child_frame

        # END PROBLEM 8

##############
# Procedures #
##############

class Procedure:
    """The the base class for all Procedure classes. Not implemented"""

class BuiltinProcedure(Procedure):
    """A Scheme procedure defined as a Python function."""

    def __init__(self, py_func, need_env=False, name='builtin'):
        self.name = name
        self.py_func = py_func
        self.need_env = need_env

    def __str__(self):
        return '#[{0}]'.format(self.name)

class LambdaProcedure(Procedure):
    """A procedure defined by a lambda expression or a define form."""

    def __init__(self, formals, body, env):
        """A procedure with formal parameter list FORMALS (a Scheme list),
        whose body is the Scheme list BODY, and whose parent environment
        starts with Frame ENV."""
        assert isinstance(env, Frame), "env must be of type Frame"

        from scheme_utils import validate_type, scheme_listp
        validate_type(formals, scheme_listp, 0, 'LambdaProcedure')
        validate_type(body, scheme_listp, 1, 'LambdaProcedure')
        self.formals = formals
        self.body = body
        self.env = env

    def __str__(self):
        return str(Pair('lambda', Pair(self.formals, self.body)))

    def __repr__(self):
        return 'LambdaProcedure({0}, {1}, {2})'.format(
            repr(self.formals), repr(self.body), repr(self.env))

class MuProcedure(Procedure):
    """A procedure defined by a mu expression, which has dynamic scope.
     _________________
    < Scheme is cool! >
     -----------------
            \   ^__^
             \  (oo)\_______
                (__)\       )\/\
                    ||----w |
                    ||     ||
    """

    def __init__(self, formals, body):
        """A procedure with formal parameter list FORMALS (a Scheme list) and
        Scheme list BODY as its definition."""
        self.formals = formals
        self.body = body

    def __str__(self):
        return str(Pair('mu', Pair(self.formals, self.body)))

    def __repr__(self):
        return 'MuProcedure({0}, {1})'.format(
            repr(self.formals), repr(self.body))
