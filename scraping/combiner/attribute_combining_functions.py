# For combine functions
def cc_percentage(s1: str, s2: str, perc: float) -> bool:
    """
    compares two strings to see if a percentage of the shortest string is identical to the longest string
    Args:
        s1 (str): first string
        s2 (str): second string
        perc (float): percentage float between 0 and 1

    Returns (bool): bool indicating equality
    """
    shortest_len = min(len(s1), len(s2))
    split_index = round(shortest_len * perc)
    print(split_index)
    return s1.lower()[:split_index] == s2.lower()[:split_index]


def cc_equal(v1: any, v2: any) -> bool:
    """
    checks if two values are equal and not None
    Args:
        v1 (any): value to compare
        v2 (any): value to compare

    Returns (bool): result of check
    """
    return v1 != None and v1 == v2
