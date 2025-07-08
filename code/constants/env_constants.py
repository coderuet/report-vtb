from dotenv import load_dotenv
import os
load_dotenv()


class EnvCons:
    BASE_URL = os.environ.get("BASE_URL", "")
    USER_NAME = os.environ.get("USER_NAME", "")
    PASSWORD = os.environ.get("PASSWORD", "")
    CARD_NUMBER = os.environ.get("CARD_NUMBER", "")
    PATH_FOLDER_SAVE = os.environ.get("PATH_FOLDER_SAVE", "")
    BUCKET_NAME = os.environ.get("BUCKET_NAME", "")
    DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "")
    GG_CREDS_PATH = os.environ.get("GG_CREDS_PATH", "")
    ICB_PUBLIC_KEY = os.environ.get("ICB_PUBLIC_KEY", "")
