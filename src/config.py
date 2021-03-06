import os

# Config information

DB_HOST = os.environ.get("DB_HOST", "52.201.108.190")
DB_PORT = os.environ.get("DB_PORT", 27017)
WEB3_PROVIDER = os.environ.get("WEB3_PROVIDER", "http://3.219.79.88:8545")
BASE_BLOCK = int(os.environ.get("BASE_BLOCK", 4348700))
BLOCK_OFFSET = int(os.environ.get("BLOCK_OFFSET", 2))
LOG_FILE = "/usr/log/info_{}_{}.log".format(
    BASE_BLOCK, BASE_BLOCK+BLOCK_OFFSET)
DB_NAME = os.environ.get("DB_NAME", "eth_db")
BLOCK_COLLECTION = os.environ.get("BLOCK_COLLECTION", "blocks")
TRANSACTION_COLLECTION = os.environ.get(
    "TRANSACTION_COLLECTION", "transactions")
