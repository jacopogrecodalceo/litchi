import re
import os
import math

def db2amp(db):
    max_val = 0
    min_val = -33
    return (db - min_val) / (max_val - min_val)

def amp2db(amp):
    max_val = 0
    min_val = -33
    return amp * (max_val - min_val) + min_val

def freq2cent(frequency, reference_frequency):
    """Converts a frequency to its equivalent cents relative to a reference frequency."""
    return 1200 * math.log2(abs(frequency) / reference_frequency) if frequency != 0 else 0.0

def ordinal_suffix(num):
    """
    Returns the ordinal representation of a number (e.g., '1st', '2nd').

    Args:
        num (int): The input number.

    Returns:
        str: The ordinal representation of the number.
    """
    if 11 <= num % 100 <= 13:  # Handle special cases for 11th, 12th, 13th
        suffix = "th"
    else:
        last_digit = num % 10
        if last_digit == 1:
            suffix = "st"
        elif last_digit == 2:
            suffix = "nd"
        elif last_digit == 3:
            suffix = "rd"
        else:
            suffix = "th"
    return f"{num}{suffix}"

def iterate_from_key(start_key, d):
    """
    Iterate over a dictionary starting from a specific key.

    Args:
        d (dict): The dictionary to iterate over.
        start_key (str): The key to start from.

    Yields:
        tuple: The current key and value.
    """
    keys = list(d.keys())
    start_index = keys.index(start_key)

    # Iterate from start_key to the end
    for i in range(start_index, len(keys)):
        yield keys[i], d[keys[i]]

    # Loop back to the beginning
    for i in range(0, start_index):
        yield keys[i], d[keys[i]]

def find_nearest(target, values):
    return min(values, key=lambda x: abs(x - target))

def get_name_from_basename(file):
    basename = os.path.basename(os.path.dirname(file))
    
    # REMOVE DATE FROM THE BEGINNING
    basename = re.sub(r'\d+-', '', basename)

    # REPLACE _
    basename = basename.replace('_', ' ')

    # REMOVE SYMBOLS
    pattern = r'[a-zA-Z0-9]+'
    result = re.findall(pattern, basename)

    return ''.join(result)

def linear_interpolate_list(x0, x1, num_elements) -> list:
    """
    Generate a list of interpolated values between two numbers.

    Parameters:
    x0 (float): The first number.
    x1 (float): The second number.
    num_elements (int): The number of elements in the interpolated list.

    Returns:
    list: A list of interpolated values.
    """
    if num_elements < 2:
        raise ValueError("num_elements must be at least 2")

    step = (x1 - x0) / (num_elements - 1)
    return [x0 + step * i for i in range(num_elements)]

def find_main_py(start_path, max_index=4):
    current_path = start_path

    index = 0
    while index < max_index:

        if os.path.isfile(current_path):
            current_path = os.path.dirname(current_path)
        # Check if main.py exists in the current directory
        if 'main.py' in os.listdir(current_path):
            return os.path.join(current_path, 'main.py')

        # Move up one directory
        parent_path = os.path.dirname(current_path)

        # If we've reached the root directory, stop
        if parent_path == current_path:
            return None

        current_path = parent_path
        index += 1