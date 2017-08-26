import re


def extract_beetwen_quotes(string):
    '''Return's the given string beetwen two quotes'''
    return re.search(r"'.*'", string).group(0).split("'")[1]


def remove_spaces_and_paragraph(string):
    '''Return's the given string without spaces and \n'''
    return re.subn(r"^\n", '', string)[0].strip()
