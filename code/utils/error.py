import requests as rq
from ..constants.env_constants import EnvCons
import functools
import traceback
import sys
from ..constants.common_constants import CommonConstants


def send_error_to_discord(error_message):
    payload = {
        "content": f"⚠️ Error occurred:\n```{error_message}```"
    }
    try:
        rq.post(EnvCons.DISCORD_WEBHOOK_URL, json=payload)
    except Exception as e:
        print("Failed to send error to Discord:", e)


def error_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        try:
            print(f"Running in {func_name}")
            return func(*args, **kwargs)
        except Exception:
            error_message = traceback.format_exc()
            print(f"Error in {func_name} error: {error_message}")
            send_error_to_discord(error_message)
            if func_name in CommonConstants.FUNCTION_NAME_NEED_RETRY:
                raise
            else:
                sys.exit(1)
    return wrapper
