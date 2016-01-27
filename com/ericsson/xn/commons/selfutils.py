# -*- coding: utf-8 -*-

import collections


def compare_lists(list_a, list_b):
    return collections.Counter(list_a) == collections.Counter(list_b)