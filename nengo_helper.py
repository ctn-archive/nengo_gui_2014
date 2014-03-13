"""Helpers for interfacing with Nengo library."""

import traceback

import nengo

import util


def annotate_object(cls, *args, **kwargs):
    """Annotate NengoObject obj, given the initialized *args, **kwargs."""
    new_label = None
    need_auto_label = 'label' not in kwargs and isinstance(
        cls, (nengo.objects.Neurons, nengo.Node, nengo.Ensemble, nengo.Network))
    for fn, line, function, code in reversed(traceback.extract_stack()):
        # Find the code which actually created this object. This is the deepest
        # call that is not in this file or nengo.objects. This is different
        # from the below case if the user, say, creates an ensemble-array
        # Network. Use this to auto-label instead of the deepest_line_number if
        # anything is found.
        if need_auto_label and \
                not util.eq_py_filenames(fn, nengo.objects.__file__) and \
                not util.eq_py_filenames(fn, __file__):
            if code:
                new_label = util.parse_variable_name(code)
                need_auto_label = False
        # Find the deepest line in the user's code that created this object
        if fn == '<string>':
            # We can't do the automatic labelling here, because code is None
            # when fn == '<string>', due to the use of compile/exec. If
            # need_auto_label, then the auto labelling will be done later using
            # the deepest_line_number.
            cls._deepest_line_number = line
            break
    else:
        cls._deepest_line_number = 0
    cls._need_auto_label = need_auto_label
    return new_label


def initialize():
    """Initializes this file."""
    # Monkey-patches the Nengo Network to annotate added objects.
    old_init = nengo.NengoObject.__init__

    def patched_init(cls, *args, **kwargs):
        new_label = annotate_object(cls, *args, **kwargs)
        if new_label:
            kwargs['label'] = new_label
        old_init(cls, *args, **kwargs)

    nengo.NengoObject.__init__ = patched_init
