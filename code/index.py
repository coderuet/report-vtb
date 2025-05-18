import string
import secrets
import time
from .constants.common_constants import CommonConstants
from .constants.endpoints import EndPoints
from .utils.captcha import bypass_captcha
import requests as rq
from .utils.helper import encrypt_data
from .constants.env_constants import EnvCons
from typing import List
from .utils.error import error_handler
import json


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
    print("Running generate captcha id")
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
    print("Running get_captcha")
    url = f"{EnvCons.BASE_URL}/{EndPoints.CAPTCHA}/{captcha_id}"
    res = rq.get(
        url, headers=CommonConstants.NULL_HEADER, timeout=10000
    )
    captcha_code = bypass_captcha(res.text)
    return captcha_code


@error_handler
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
    if res.status_code != 200:
        raise Exception("Invalid captcha")
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
    print("Running get transactions")
    request_id = generate_request_id()
    sessions_id = login(EnvCons.USER_NAME, EnvCons.PASSWORD)
    if sessions_id is None:
        raise Exception("Login failed")
    print("sessions_id", sessions_id)
    params = {
        "accountNumber": EnvCons.CARD_NUMBER,
        "startDate": start_date,
        "endDate": end_date,
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
    print("body", body)
    print("params", params)

    res = rq.post(
        f"{EnvCons.BASE_URL}/{EndPoints.GET_HIST_TRANSACTIONS}", json=body, headers=CommonConstants.NULL_HEADER)
    f = open("result.json", "w")
    f.write(json.dumps(res.json()))
    f.close()


if __name__ == "__main__":
    get_transactions(start_date="2025-04-01",
                     end_date="2025-04-30", limit=100)
