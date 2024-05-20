import sys

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

    if scheme_symbolp(expr):
        return env.lookup(expr)
    elif self_evaluating(expr):
        return expr

    if not scheme_listp(expr):
        raise SchemeError('malformed list: {0}'.format(repl_str(expr)))

    first, rest = expr.first, expr.rest
    if scheme_symbolp(first) and first in scheme_forms.SPECIAL_FORMS:
        return scheme_forms.SPECIAL_FORMS[first](rest, env)
    else:
        # BEGIN PROBLEM 3
        """ 
        Author: Arshmeet Kaur
        The following code evaluates a call expression.
        (operator operand operand...)
        
        1. An operator evaluates to itself.
        2. operands are either self-evaluating or call expressions that must be evaluated themselves.
        3. operands and operator must be passed to scheme_apply to be evaluated.
        """
        # look at the operator's bindings in the env
        procedure = scheme_eval(first, env)
        # map a lambda function to the operands which evaluates them in the current env recursively
        args = rest.map((lambda x: scheme_eval(x, env)))
        # apply an operator to its operands
        return(scheme_apply(procedure, args, env))
        #END PROBLEM 3


def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    Frame ENV, the current environment."""
    validate_procedure(procedure)
    if not isinstance(env, Frame):
       assert False, "Not a Frame: {}".format(env)
    if isinstance(procedure, BuiltinProcedure):
        # BEGIN PROBLEM 2
        """ 
        Authors: Lukas Hammett & Arshmeet Kaur
        This part of scheme_apply deals with Scheme
        procedures that can be implemented using a
        built-in Python procedure.
        
        1. Take each Scheme argument in args and put
           into a list of Python arguments py_args.
        2. Add the current environment/frame if the
           the procedure depends on it.
        3. Pass in py_args to the built-in Python
           function that implements the procedure.
        """
        # Initialize list of parameters
        py_args = []

        """ Arshmeet: fixed this loop. """
        try:
            while True:
                py_args.append(args.first)
                if (args.rest == nil):
                    break
                args = args.rest
        except AttributeError:
            """ Deal with when 0 args are passed in"""
            pass

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
        """ Author: Mike Beitner 
         If a lambda procedure, a child frame of the current environment is made.
         The body args are eval_all-ed"""
        new_frame = procedure.env.make_child_frame(procedure.formals, args)
        result = eval_all(procedure.body, new_frame) # call eval_all with new frame
        return result
        # END PROBLEM 9
    elif isinstance(procedure, MuProcedure):
        # BEGIN PROBLEM 11
        "Author - Cesar Salto"
        """Evaluates procedure body in a new child environment frame with bound arguments"""
        child = env.make_child_frame(procedure.formals, args)
        return eval_all(procedure.body, child)
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
    """
    Author: Lukas Hammett
    eval_all, as stated in its docstring above, takes in
    a list of Scheme expressions and the current environment,
    and evaluates them in order, resulting in a final value
    that is the value of the last expression.

    1. If the expression list has no expressions, return None.
    2. Evaluate each expression in order, calling scheme_eval,
       until there is only one expression left.
    3. Return the result of evaluating that one expression.
    """
    # Check if there actually is an expression in the Scheme procedure
    if (expressions == nil):
        return None
    # Evaluate each expression in order, then get the next expression
    while (expressions.rest != nil):
        scheme_eval(expressions.first, env)
        expressions = expressions.rest
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
