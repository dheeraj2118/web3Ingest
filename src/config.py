import os

# Config information

DB_HOST = os.environ.get("DB_HOST", "18.211.113.218")
DB_PORT = os.environ.get("DB_PORT", 27017)
WEB3_PROVIDER = os.environ.get("WEB3_PROVIDER", "http://52.21.97.126:8545")
BASE_BLOCK = int(os.environ.get("BASE_BLOCK", 0))
BLOCK_OFFSET = int(os.environ.get("BLOCK_OFFSET", 0))
LOG_FILE = "info_{}_{}.log".format(
    BASE_BLOCK, BASE_BLOCK+BLOCK_OFFSET)
DB_NAME = os.environ.get("DB_NAME", "eth_db_test")
BLOCK_COLLECTION = os.environ.get("BLOCK_COLLECTION", "blocks")
TRANSACTION_COLLECTION = os.environ.get(
    "TRANSACTION_COLLECTION", "transactions")
