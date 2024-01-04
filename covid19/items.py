import scrapy
import re
from datetime import datetime


def reformat_date(date_string):
    """
    Reformat a date string from one format to another, handling new lines.

    Args:
        date_string (str): A string representing a date that may contain new lines and whitespaces.

    Returns:
        str: A reformatted date string in the format "%H:%M %d-%m-%Y".

    Raises:
        ValueError: If the input date string is not in the expected format.

    Example:
        >>> reformat_date("12:30 31/01/2022\n")
        '12:30 31-01-2022'
    """
    # Remove new lines and extra whitespaces from the input date string
    date_string = remove_new_lines(date_string)

    try:
        # Convert the processed date string to a datetime object
        date_object = datetime.strptime(date_string, "%H:%M %d/%m/%Y")

        # Format the datetime object into the desired output format
        reformatted_date = date_object.strftime("%H:%M %d-%m-%Y")

        return reformatted_date

    except ValueError as e:
        # Handle the case where the processed date string is not in the expected format
        raise ValueError(f"Invalid date format: {e}")


def handles_case(self, case_raw):
    """
    Extracts and handles numeric cases from a raw string.

    Args:
        case_raw (str): A string containing numeric cases in various formats.

    Returns:
        int or str: An integer representing the extracted numeric case or the original string if no cases are found.

    Raises:
        ValueError: If the extracted numeric value cannot be converted to an integer.

    Example:
        >>> handles_case("Total cases: 1,234.56")
        123456
    """
    # Define a regular expression pattern to match numeric values
    regex = r'\d+\.\d+|\d+'

    # Use regular expressions to find numeric values in the input string
    case_raw = re.findall(regex, case_raw)

    # If numeric values are found, convert the first one to an integer
    if len(case_raw) > 0:
        try:
            case_raw = int(case_raw[0].replace('.', ''))
        except ValueError as e:
            raise ValueError(f"Error converting to integer: {e}")

    return case_raw


def remove_new_lines(string):
    """
    Remove new lines and extra whitespaces from a given string.

    Args:
        string (str): The input string containing new lines and whitespaces.

    Returns:
        str: The input string with new lines and extra whitespaces removed.

    Example:
        >>> remove_new_lines("This is\n a sample \nstring.")
        'This is a sample string.'
    """
    return re.sub(r'\n\s+', '', string)


def get_case(case_raw):
    """
    Extracts and returns a numeric case from a raw string.

    Args:
        case_raw (str): A string containing numeric cases in various formats.

    Returns:
        int or None: An integer representing the extracted numeric case or None if no cases are found.

    Raises:
        ValueError: If the extracted numeric value cannot be converted to an integer.

    Example:
        >>> get_case("Total cases: 1,234.56")
        123456
    """
    # Define a regular expression pattern to match numeric values
    regex = r'\d+\.\d+|\d+'

    # Use regular expressions to find numeric values in the input string
    case_raw = re.findall(regex, case_raw)

    # If numeric values are found, convert the first one to an integer
    if len(case_raw) > 0:
        try:
            case_raw = int(case_raw[0].replace('.', ''))
        except ValueError as e:
            raise ValueError(f"Error converting to integer: {e}")
        return case_raw
    else:
        return None


def no_accent_vietnamese(s):
    """
    Remove accents from Vietnamese characters in a given string.

    Args:
        s (str): The input string containing Vietnamese characters with accents.

    Returns:
        str: The input string with accents removed.

    Example:
        >>> no_accent_vietnamese("Hà Nội")
        'Ha Noi'
    """
    # Replace accented characters with their non-accented counterparts
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(r'[Đ]', 'D', s)
    s = re.sub(r'[đ]', 'd', s)

    # Remove additional diacritic marks
    marks_list = [u'\u0300', u'\u0301', u'\u0302', u'\u0303', u'\u0306', u'\u0309', u'\u0323']
    for mark in marks_list:
        s = s.replace(mark, '')

    return s


def city_case(detail):
    """
        Extracts city-case pairs from a given string, handling accents.

        Args:
            detail (str): A string containing information about cities and corresponding cases.

        Returns:
            list of dict or str: A list of dictionaries, each containing a city and its corresponding case,
                                 or "figures not available" if no matches are found.

        Example:
            >>> city_case("Hà Nội (1000) and Hồ Chí Minh City (2000)")
            [{'city': 'Ha Noi', 'case': '1000'}, {'city': 'Ho Chi Minh City', 'case': '2000'}]
        """
    # Remove accents from the input detail string
    detail_no_accent_vietnamese = no_accent_vietnamese(detail)

    # Define a regular expression pattern to match city-case pairs
    regex = r'(\b[A-Z][\w\s]+\b)\s*\((\d+(?:\.\d+)?)\)\s*'

    # Initialize an empty list to store the result
    result = []

    # Use regular expressions to find city-case pairs in the processed detail string
    matches = re.findall(regex, detail_no_accent_vietnamese)

    # Iterate through the matches and append them to the result list as dictionaries
    for match in matches:
        result.append({"city": match[0], "case": match[1]})

    # Return the result or a message if no matches are found
    if len(result) > 0:
        return result
    else:
        return "Figures not available"


class Covid19Item(scrapy.Item):
    time = scrapy.Field(serializer=reformat_date)
    new_cases = scrapy.Field(serializer=get_case)
    city_cases = scrapy.Field(serializer=city_case)
    url = scrapy.Field()
