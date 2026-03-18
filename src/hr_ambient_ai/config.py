import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    hibob_service_user_id: str = os.environ["HIBOB_SERVICE_USER_ID"]
    hibob_token: str = os.environ["HIBOB_TOKEN"]
    hibob_base_url: str = os.getenv("HIBOB_BASE_URL", "https://api.hibob.com/v1")


settings = Settings()
