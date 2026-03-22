'''
Tools to perform a difflib, but with a quick exit if
it is impossible to get the amount needed
'''
from collections import Counter


def quick_ratio(seg1, seg2) -> float:
    '''
    about double the speed of Python's quick_ratio
    '''
    tot_length = len(seg1) + len(seg2)
    if tot_length == 0:
        return 1.0

    c1 = Counter(seg1)
    c2 = Counter(seg2)

    tot = 0
    for k in {*c1, *c2}:  # set of all keys
        tot += min(c1[k], c2[k]) * 2
    return tot / tot_length


def compare_two(seg1, seg2):
    pass
