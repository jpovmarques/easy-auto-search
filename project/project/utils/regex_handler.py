import re


def _extract_beetwen_quotes(string):
    '''Return's the given string beetwen two quotes with extention .jpg'''
    try:
    	return re.fullmatch(
    		r"^.+'(?P<image_url>[https://|http://].+\.jpg)'.+$",
    		string
    	).group('image_url')
    except AttributeError:
    	return None


def _remove_spaces_and_paragraph_from_list(_list):
    '''Return's the given list without spaces and \n'''
    new_list = []
    for element in _list:
        new_list.append(_remove_spaces_and_paragraph(element))
    return new_list


def _remove_spaces_and_paragraph(string):
    '''Return's the given string without spaces and \n'''
    return re.subn(r"\n", '', string)[0].strip()
