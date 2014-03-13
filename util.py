"""General utilities file."""

import keyword
import re

import traceback
from StringIO import StringIO


def is_identifier(s):
    """Returns true iff s is a valid Python identifier."""
    if s in keyword.kwlist:
        return False
    return re.match(r'^[a-z_][a-z0-9_]*$', s, re.I) is not None


def parse_variable_name(text):
    """Guesses the variable name being assigned to in text, or returns None."""
    if '=' in text:
        text = text.split('=', 1)[0].split('self.', 1)[-1].strip()
        if is_identifier(text):
            return text
    return None


def eq_py_filenames(fname1, fname2):
    """Returns true iff the given file names are equivalent Python scripts."""
    def normalize(fname):
        if fname.endswith('.pyc'):
            return fname[:-1]
        return fname
    return normalize(fname1) == normalize(fname2)


def traceback_exc():
    """Returns the string printed by traceback.print_exc."""
    s = StringIO()
    traceback.print_exc(file=s)
    return s.getvalue()
