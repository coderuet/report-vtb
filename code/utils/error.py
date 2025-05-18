import requests as rq
from ..constants.env_constants import EnvCons
import functools
import traceback


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
        try:
            return func(*args, **kwargs)
        except Exception:
            error_message = traceback.format_exc()
            func_name = func.__name__
            print(f"Error in {func_name} error: {error_message}")
            send_error_to_discord(error_message)
    return wrapper
