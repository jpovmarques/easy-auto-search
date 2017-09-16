import re

class RegexHandler:

    CAPACITY_REGEX_PATTERN = re.compile(r"^\n.*?(?P<result>(\d+ )?[\d]+ cm3)(.*$)")
    KMS_REGEX_PATTERN = re.compile(r"^\n.*?(?P<result>(\d+ )?[\d]+ km)(.*$)")
    PICTURE_REGEX_PATTERN = re.compile(r"^.+'(?P<image_url>(https://|http://).+\.jpg)'.+$")

    @classmethod
    def extract_beetwen_quotes(cls, string):
        """Return's the given string beetwen two quotes with extention .jpg"""
        try:
            return re.fullmatch(
                cls.PICTURE_REGEX_PATTERN,
                string
            ).group('image_url')
        except AttributeError:
            return None

    @classmethod
    def get_capacity_value(cls, string):
        """Returns the given string value for capacity"""
        if string:
            try:
                return re.fullmatch(cls.CAPACITY_REGEX_PATTERN, string).group('result')
            except AttributeError:
                return None

    @classmethod
    def get_kms_value(cls, string):
        """Returns the given string value for kms"""
        if string:
            try:
                return re.fullmatch(cls.KMS_REGEX_PATTERN, string).group('result')
            except AttributeError:
                return None
