import requests as rq
from ..constants.env_constants import EnvCons
import functools
import traceback
import sys
from ..constants.common_constants import CommonConstants
from typing import Dict, Callable, Any
import requests


def send_error_to_discord(error_message: str):
    """
    Send error message to Discord webhook.
    Args:
        error_message (str): Error message to send to Discord
    """
    payload: Dict = {"content": f"⚠️ Error occurred:\n```{error_message}```"}
    try:
        rq.post(EnvCons.DISCORD_WEBHOOK_URL, json=payload)
    except Exception as e:
        print("Failed to send error to Discord:", e)


def error_handler(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Error handler decorator that catch and handle error after that send message to discord webhook

    Args:
        func (_type_): function

    Returns:
        _type_: function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        try:
            print(f"Running in {func_name}")
            return func(*args, **kwargs)
        except requests.exceptions.HTTPError as e:
            # Caught an HTTPError, now include res.text
            error_message = f"HTTP Error in {func_name}: {e}\n"
            if e.response is not None:
                error_message += f"Response content: {e.response.text}\n"
            error_message += traceback.format_exc()  # Still include the full traceback
            print(f"Error in {func_name} error: {error_message}")
            send_error_to_discord(error_message)
            if func_name in CommonConstants.FUNCTION_NAME_NEED_RETRY:
                raise  # Re-raise if retry is needed
            else:
                sys.exit(1)
        except Exception:
            # This block handles all other exceptions that are not HTTPError
            error_message = traceback.format_exc()
            print(f"Error in {func_name} error: {error_message}")
            send_error_to_discord(error_message)
            if func_name in CommonConstants.FUNCTION_NAME_NEED_RETRY:
                raise
            else:
                sys.exit(1)

    return wrapper
