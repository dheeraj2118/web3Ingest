from web3 import Web3
from pymongo import MongoClient
from config import *
import logging
import sys

logging.basicConfig(filename=BASIC_LOGS)


def get_web3_connection(provider):
    try:
        w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER))
        logging.info("Connected to Web3 provider at {}".format(WEB3_PROVIDER))
        return w3
    except Exception as e:
        logging.error("Failed to ger web3 connection: {}".format(e))
        sys.exit(0)


def get_db_connection(db_host, db_port, db_name):
    try:
        mongoClient = MongoClient(db_host, db_port)
        logging.info("Connected to database client")
        return mongoClient[db_name]
    except Exception as e:
        logging.error(
            "Failed to connect to DB @ {} {} with error {}".format(
                db_host, db_port, e)
        )
        sys.exit(0)


def get_block_dict(w3, block_number):
    try:
        block = w3.eth.getBlock(block_number).__dict__
        logging.info("Block loaded {}".format(block_number))
        return block
    except Exception as e:
        logging.error(
            "Error getting block {} error {}".format(block_number, e))


def get_transaction_info(w3, transaction_hash):
    try:
        return w3.eth.getTransaction(transaction_hash).__dict__
    except Exception as e:
        logging.error(
            "Error while getting transaction Information {}".format(e))


def load_blocks(base_block, block_offset):
    w3 = get_web3_connection(WEB3_PROVIDER)
    db = get_db_connection(DB_HOST, DB_PORT, DB_NAME)
    blocks = db[BLOCK_COLLECTION]
    transactions = db[TRANSACTION_COLLECTION]
    block_count = 0
    transaction_count = 0
    for i in range(block_offset):
        block = get_block_dict(w3, base_block + i)
        if block:
            block["totalDifficulty"] = str(block["totalDifficulty"])
            block["difficulty"] = str(block["difficulty"])
            blocks.insert_one(block)
            block_count += 1
            for transaction in block["transactions"]:
                transaction_details = get_transaction_info(
                    w3, transaction.hex())
                transactions.insert_one(transaction_details)
                transaction_count += 1
        else:
            continue
        print(
            "Ingested {} blocks and {} transactions from block number {} to {}".format(
                block_count, transaction_count, base_block, base_block + block_offset
            )
        )


load_blocks(BASE_BLOCK, BLOCK_OFFSET)
