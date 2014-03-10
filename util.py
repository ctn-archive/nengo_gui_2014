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


def traceback_exc():
    """Returns the string printed by traceback.print_exc."""
    s = StringIO()
    traceback.print_exc(file=s)
    return s.getvalue()
