import urllib.parse
import json
from .crypto import md5, encrypt_rsa
from ..constants.env_constants import EnvCons
# Replace with actual PEM-formatted public key string
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .error import error_handler
from typing import List, Dict
from collections import defaultdict
import os


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


def split_by_month(start_date_str: str, end_date_str: str) -> list[str]:
    """

    Args:
        start_date_str (str): _description_
        end_date_str (str): _description_

    Returns:
        list[str]: List of date in range with step = 2 months
    """
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    result = []
    current = start_date

    while current < end_date:
        result.append(current.strftime("%Y-%m-%d"))
        next_date = current + relativedelta(months=1)
        if next_date >= end_date:
            break
        current = next_date

    # Ensure end_date is included
    if not result or result[-1] != end_date.strftime("%Y-%m-%d"):
        result.append(end_date.strftime("%Y-%m-%d"))

    return result


@error_handler
def clean_data(transactions: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Remove unnecessary fields and group transactions by formatted processDate.

    Args:
        transactions (List): List of transactions from VTB.

    Returns:
        Dict: Transactions grouped by processDate in 'YYYY-MM-DD' format.
    """
    allowed_keys = {
        'remark', 'amount', 'processDate', 'trxId', 'dorC',
        'corresponsiveAccount', 'corresponsiveName', 'receivingBranchName', 'sendingBranchName'
    }

    grouped = defaultdict(list)

    for trx in transactions:
        filtered_trx = {k: v for k, v in trx.items() if k in allowed_keys}
        formatted_date = str(datetime.strptime(
            filtered_trx["processDate"], "%d-%m-%Y %H:%M:%S").strftime("%Y-%m-%d"))
        # Grouped by year-month
        grouped[formatted_date[:-3]].append(filtered_trx)

    return dict(grouped)


@error_handler
def write_file(grouped_transactions: Dict) -> List[str]:
    """Save file with grouped transactions

    Args:
        grouped_transactions (Dict): Transactions grouped by month with key is YYYY-MM 
        and key is list of transactions in that month
    Returns:
        List[str]: List file name
    """
    list_file: List[str] = []
    for key in grouped_transactions:
        print(key)
        file_path = os.path.join(EnvCons.PATH_FOLDER_SAVE, f"{key}.json")
        f = open(file_path, "w")
        f.write(json.dumps(grouped_transactions[key]))
        f.close()
        list_file.append(f"{key}.json")
    return list_file
