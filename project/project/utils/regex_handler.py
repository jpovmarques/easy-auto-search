import re


def extract_beetwen_quotes(string):
    '''Return's the given string beetwen two quotes with extention .jpg'''
    try:
    	return re.fullmatch(
    		r"^.+'(?P<image_url>[https://|http://].+\.jpg)'.+$",
    		string
    	).group('image_url')
    except AttributeError:
    	return

def remove_spaces_and_paragraph(string):
    '''Return's the given string without spaces and \n'''
    return re.subn(r"^\n", '', string)[0].strip()
