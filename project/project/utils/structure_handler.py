def safe_list_get (l :list, index, default=None) -> str:
    """
    If the given index exists, returns the value in it.
    Else, returns de given default value.
    """
    try:
        return l[index]
    except IndexError:
        return default
