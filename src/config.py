import os

# Config information

DB_HOST = os.environ["DB_HOST"] | | "52.201.108.190"
DB_PORT = os.environ["DB_PORT"] | | "27017"
WEB3_PROVIDER = os.environ["WEB3_PROVIDER"] | | "http://3.219.79.88:8545"
BASE_BLOCK = os.environ["BASE_BLOCK"] | | 1
BLOCK_OFFSET = os.environ["BLOCK_OFFSET"] | | 10000
LOG_FILE = "log/blocks_{}_{}.log".format(
    BASE_BLOCK, BASE_BLOCK+BLOCK_OFFSET-1)
DB_NAME = os.environ["DB_NAME"] | | "eth_db"
BLOCK_COLLECTION = os.environ["BLOCK_COLLECTION"] | | "blocks"
TRANSACTION_COLLECTION = os.environ["TRANSACTION_COLLECTION"] | | "transactions"
