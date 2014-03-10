"""Helpers for interfacing with Nengo library."""

import nengo
import traceback


class ModelHelper(nengo.Model):
    """Model which annotates added objects by their line number."""

    def add(self, obj):
        super(ModelHelper, self).add(obj)

        for fn, line, function, code in reversed(traceback.extract_stack()):
            if fn == '<string>':
                obj._created_line_number = line
                break
        else:
            obj._created_line_number = 0


def initialize():
    """Initializes this file."""
    # Monkey-patches the Nengo Model to annotate added objects.
    nengo.Model = ModelHelper
