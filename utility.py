from operator import add, sub


def list_add(l1, l2):
    return list(map(add, l1, l2))


def list_sub(l1, l2):
    return list(map(sub, l1, l2))
