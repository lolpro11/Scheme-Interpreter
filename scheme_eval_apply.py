import sys

from operator import add, sub
from pair import *
from scheme_utils import *
from ucb import main, trace

import scheme_forms

##############
# Eval/Apply #
##############

def scheme_eval(expr, env, _=None): # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in Frame ENV.

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """

    # handling the atomic expressions (containing only one element)
    if scheme_symbolp(expr):
        return env.lookup(expr)
    elif self_evaluating(expr): # covers boolean, number, symbol, null, or string
        return expr

    # All non-atomic expressions are lists (combinations)
    # if it's not a well-formed list (Pair instance), raise a scheme error
    if not scheme_listp(expr):
        raise SchemeError('malformed list: {0}'.format(repl_str(expr)))

    # if it is well formed, we can get the operation from the first element in the pair
    first, rest = expr.first, expr.rest
    # handles special forms
    if scheme_symbolp(first) and first in scheme_forms.SPECIAL_FORMS:
        return scheme_forms.SPECIAL_FORMS[first](rest, env)
    else:
        # BEGIN PROBLEM 3
        """ 
        Arshmeet Kaur
        The following code evaluates a call expression.
        (operator operand operand...)
        """

        """ If the element passed in is a pair, the first index is the operation and the rest are the arguments. """
        if isinstance(expr, Pair):
            """ Recursively call the function on the rest of the Pair """
            args = rest.map((lambda x: scheme_eval(x, env))
            """ Actually apply the operation to all the extracted args """
            return(scheme_apply(first, args, Frame()))
        else:
            raise TypeError(str(expr) + 'is not self-evaluating or a call expression')
        # END PROBLEM 3


def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    Frame ENV, the current environment."""
    validate_procedure(procedure)
    if not isinstance(env, Frame):
       assert False, "Not a Frame: {}".format(env)
    if isinstance(procedure, BuiltinProcedure):
        # BEGIN PROBLEM 2
        # Initialize list of parameters
        py_args = []
        # Empty args into the list of parameters
        while (args.rest != nil):
            py_args.append(args.first)
            args = args.rest
        # Add the current environment if necessary for the given Scheme procedure
        if (procedure.need_env):
            py_args.append(env)
        # END PROBLEM 2
        try:
            # BEGIN PROBLEM 2
            # Pass in each parameter to the corresponding built-in Python function
            return procedure.py_func(*py_args)
            # END PROBLEM 2
        except TypeError as err:
            raise SchemeError('incorrect number of arguments: {0}'.format(procedure))
    elif isinstance(procedure, LambdaProcedure):
        # BEGIN PROBLEM 9
        "*** YOUR CODE HERE ***"
        # END PROBLEM 9
    elif isinstance(procedure, MuProcedure):
        # BEGIN PROBLEM 11
        "*** YOUR CODE HERE ***"
        # END PROBLEM 11
    else:
        assert False, "Unexpected procedure: {}".format(procedure)

def eval_all(expressions, env):
    """Evaluate each expression in the Scheme list EXPRESSIONS in
    Frame ENV (the current environment) and return the value of the last.

    >>> eval_all(read_line("(1)"), create_global_frame())
    1
    >>> eval_all(read_line("(1 2)"), create_global_frame())
    2
    >>> x = eval_all(read_line("((print 1) 2)"), create_global_frame())
    1
    >>> x
    2
    >>> eval_all(read_line("((define x 2) x)"), create_global_frame())
    2
    """
    # BEGIN PROBLEM 6
    # Check if there actually is an expression in the Scheme procedure
    if (expressions == nil):
        return None
    # Evaluate each expression in order, then get the next expression
    while (expressions.second != nil):
        scheme_eval(expressions.first, env)
        expressions = expressions.second
    # Return the value after evaluating the last remaining expression
    return scheme_eval(expressions.first, env)
    # END PROBLEM 6


##################
# Tail Recursion #
##################

class Unevaluated:
    """An expression and an environment in which it is to be evaluated."""

    def __init__(self, expr, env):
        """Expression EXPR to be evaluated in Frame ENV."""
        self.expr = expr
        self.env = env

def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not an Unevaluated."""
    validate_procedure(procedure)
    val = scheme_apply(procedure, args, env)
    if isinstance(val, Unevaluated):
        return scheme_eval(val.expr, val.env)
    else:
        return val

def optimize_tail_calls(unoptimized_scheme_eval):
    """Return a properly tail recursive version of an eval function."""
    def optimized_eval(expr, env, tail=False):
        """Evaluate Scheme expression EXPR in Frame ENV. If TAIL,
        return an Unevaluated containing an expression for further evaluation.
        """
        if tail and not scheme_symbolp(expr) and not self_evaluating(expr):
            return Unevaluated(expr, env)

        result = Unevaluated(expr, env)
        # BEGIN OPTIONAL PROBLEM 1
        "*** YOUR CODE HERE ***"
        # END OPTIONAL PROBLEM 1
    return optimized_eval














################################################################
# Uncomment the following line to apply tail call optimization #
################################################################

# scheme_eval = optimize_tail_calls(scheme_eval)
