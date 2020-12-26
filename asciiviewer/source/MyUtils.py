import six


def isSequenceType(obj):
    if six.PY2:
        import operator
        return operator.isSequenceType(obj)
    else:
        import collections.abc
        return isinstance(obj, collections.abc.Sequence)
