from tenacity import retry, stop_after_attempt, wait_fixed
import string
import secrets
import time
from ..constants.common_constants import CommonConstants
from ..constants.endpoints import EndPoints
from .captcha import bypass_captcha
import requests as rq
from .helper import encrypt_data
from ..constants.env_constants import EnvCons
from typing import List, Dict
from .error import error_handler
from cachetools import TTLCache
from cachetools import cached
from .helper import split_by_month
cache = TTLCache(maxsize=100, ttl=60 * 5 - 10)


@error_handler
def generate_request_id() -> str:
    """_summary_
    Generate request id
    Returns:
        str: _description_
    """
    alphabet = string.ascii_uppercase + string.digits
    random_part = ''.join(secrets.choice(alphabet) for _ in range(12))
    timestamp = int(time.time() * 1000)
    return f"{random_part}|{timestamp}"


@error_handler
def generate_captcha_id() -> str:
    """
    """
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(9))


@error_handler
def get_captcha(captcha_id: str) -> str:
    """_summary_

    Args:
        captcha_id (str): Captcha ID

    Returns:
        str: captcha code with 
    """
    url = f"{EnvCons.BASE_URL}/{EndPoints.CAPTCHA}/{captcha_id}"
    res = rq.get(
        url, headers=CommonConstants.NULL_HEADER, timeout=10000
    )
    captcha_code = bypass_captcha(res.text)
    return captcha_code


@retry(stop=stop_after_attempt(5), wait=wait_fixed(1))
@error_handler
@cached(cache)
def login(username: str, password: str):
    """
    Login VTB ipay with username and password to get sessionId
    Args:
        username (str): username login with ipay app
        password (str): password 
    """
    captcha_id = generate_captcha_id()
    captcha_code = get_captcha(captcha_id)
    request_id = generate_request_id()
    headers = CommonConstants.NULL_HEADER
    params = {
        "accessCode": password,
        "browserInfo": CommonConstants.BROWSER_INFO,
        "captchaCode": captcha_code,
        "captchaId": captcha_id,
        "clientInfo": CommonConstants.CLIENT_INFO,
        "lang": 'vi',
        "requestId": request_id,
        "userName": username,
        "screenResolution": '1201x344'
    }
    body = encrypt_data(params)
    res = rq.post(f"{EnvCons.BASE_URL}/{EndPoints.LOGIN}",
                  headers=headers, json=body)
    print("res login", res.text)
    res.raise_for_status()

    data = res.json()
    return data["sessionId"]


@error_handler
def get_transactions(start_date: str, end_date: str, search: str = "", limit: int = 10, ) -> List:
    """_summary_
    Get all transactions from start date to end date
    Args:
        start_date (str): start date query
        end_date (str): end date query
        search (str): _description_  Defaults to 10.
        limit (int, optional): _description_. Defaults to 10.

    Returns:
        List: List of transaction from start date to end date
    """
    request_id = generate_request_id()
    sessions_id = login(EnvCons.USER_NAME, EnvCons.PASSWORD)

    list_date_in_range = split_by_month(
        start_date_str=start_date, end_date_str=end_date)
    for ind, start_date_split in enumerate(list_date_in_range):
        if ind == len(list_date_in_range) - 1:
            break  # Avoid IndexError on last iteration

        end_date_split = list_date_in_range[ind + 1]

        params = {
            "accountNumber": EnvCons.CARD_NUMBER,
            "startDate": start_date_split,
            "endDate": end_date_split,
            "maxResult": str(limit),
            "pageNumber": 0,
            "requestId": request_id,
            "tranType": '',
            "lang": 'vi',
            "searchFromAmt": '',
            "searchKey": search,
            "searchToAmt": '',
            "sessionId": sessions_id
        }
        body = encrypt_data(params)

        res = rq.post(
            f"{EnvCons.BASE_URL}/{EndPoints.GET_HIST_TRANSACTIONS}", json=body, headers=CommonConstants.NULL_HEADER)
        res.raise_for_status()
        data = res.json()
        pages = int(data["totalRecords"] / data["pageSize"])
        transactions: List[Dict] = data["transactions"]
        for i in range(pages):
            page_index = i + 1
            params["pageNumber"] = page_index
            body = encrypt_data(params)
            res = rq.post(
                f"{EnvCons.BASE_URL}/{EndPoints.GET_HIST_TRANSACTIONS}", json=body, headers=CommonConstants.NULL_HEADER)
            res.raise_for_status()
            transactions = transactions + res.json()["transactions"]
    return data["transactions"]
