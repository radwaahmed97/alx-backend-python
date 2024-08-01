#!/usr/bin/env python3
"""
function sum_list which takes
a list input_list of floats as argument and returns their sum as a float.
"""
from typing import List


def sum_list(input_list: List[float]) -> float:
    """
    Function to calculate the sum of a list of floats.

    Args:
    input_list (list): List of floats.

    Returns:
    float: Sum of the input list.
    """
    return sum(input_list)
