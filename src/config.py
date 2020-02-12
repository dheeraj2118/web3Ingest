import os

# Config information

DB_HOST = os.environ.get("DB_HOST", "52.201.108.190")
DB_PORT = os.environ.get("DB_PORT", 27017)
WEB3_PROVIDER = os.environ.get("WEB3_PROVIDER", "http://3.219.79.88:8545")
BASE_BLOCK = os.environ.get("BASE_BLOCK", 4348700)
BLOCK_OFFSET = os.environ.get("BLOCK_OFFSET", 20)
LOG_FILE = "info.log"
DB_NAME = os.environ.get("DB_NAME", "eth_db")
BLOCK_COLLECTION = os.environ.get("BLOCK_COLLECTION", "blocks")
TRANSACTION_COLLECTION = os.environ.get(
    "TRANSACTION_COLLECTION", "transactions")
