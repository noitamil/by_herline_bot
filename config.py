import os
from dataclasses import dataclass
import os

from dotenv import load_dotenv
load_dotenv()

@dataclass
class Config:
    bot_token: str
    admin_id: int

def load_config() -> Config:
    bot_token = os.getenv("BOT_TOKEN")
    admin_id = os.getenv("ADMIN_ID")

    if not bot_token:
        raise RuntimeError("BOT_TOKEN is not set")
    if not admin_id:
        raise RuntimeError("ADMIN_ID is not set")
    return Config(
        bot_token=bot_token,
        admin_id=int(admin_id)
    )
