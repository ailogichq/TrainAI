"""
Manage all configurations and connections
"""

import os
from dotenv import load_dotenv

# from pymongo.mongo_client import MongoClient

load_dotenv()


class ConnectionConfig:
    openai_url: str = os.environ.get("OPENAI_URL")
    openai_sec_key: str = os.environ.get("OPENAI_SEC_KEY")


settings = ConnectionConfig()
