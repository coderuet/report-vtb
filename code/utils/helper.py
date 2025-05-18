import urllib.parse
from collections import defaultdict
import json
from .crypto import md5, encrypt_rsa
from ..constants.env_constants import EnvCons
# Replace with actual PEM-formatted public key string


def qs_stringify(data, array_format='repeat', sort_function=None):
    """
    Convert a dictionary to a query string with support for repeated array parameters

    Parameters:
    data (dict): The data to convert
    array_format (str): How to format arrays, 'repeat' for repeated keys
    sort_function (callable): Optional function to sort the keys

    Returns:
    str: The formatted query string
    """
    # Flatten nested dictionaries and handle arrays
    result = []

    def flatten(obj, prefix=""):
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_prefix = f"{prefix}[{key}]" if prefix else key
                flatten(value, new_prefix)
        elif isinstance(obj, list):
            if array_format == 'repeat':
                # For each item in the array, add it with the same key
                for item in obj:
                    if isinstance(item, (dict, list)):
                        # Handle nested objects in arrays
                        flatten(item, f"{prefix}[]")
                    else:
                        result.append((prefix, item))
        else:
            result.append((prefix, obj))

    flatten(data)

    # Sort the parameters if a sort function is provided
    if sort_function:
        result.sort(key=lambda x: x[0], reverse=False)

    # Convert to query string format
    parts = []
    for key, value in result:
        if value is not None:
            parts.append(
                f"{urllib.parse.quote(str(key))}={urllib.parse.quote(str(value))}")

    return "&".join(parts)


def encrypt_data(data: dict) -> dict:
    """
    Encrypts data with RSA after adding an MD5 signature.

    Args:
        data: Dictionary containing string, number or None values

    Returns:
        Dictionary with the encrypted payload
    """
    query_string = qs_stringify(data, array_format='repeat',
                                sort_function=lambda a, b: (a > b) - (a < b))
    # Add MD5 signature
    data['signature'] = md5(query_string)
    # Convert data to JSON string
    payload = json.dumps(data)
    # Encrypt with RSA
    encrypt = encrypt_rsa(payload, EnvCons.ICB_PUBLIC_KEY)
    return {
        "encrypted": encrypt
    }
