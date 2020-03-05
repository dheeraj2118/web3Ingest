from web3 import Web3
from pymongo import MongoClient
from config import *
import logging
import sys

logging.basicConfig(filename=LOG_FILE, level=logging.INFO)
executing_load = False
mongoClient = None


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
        global mongoClient
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
        return False


def get_transaction_info(w3, transaction_hash):
    try:
        return w3.eth.getTransaction(transaction_hash).__dict__
    except Exception as e:
        logging.error(
            "Error while getting transaction Information {}".format(e))
        return False


def load_blocks(block_height_db=0, block_height_node=0):
    executing_load = True
    w3 = get_web3_connection(WEB3_PROVIDER)
    db = get_db_connection(DB_HOST, DB_PORT, DB_NAME)
    print(db)
    blocks = db[BLOCK_COLLECTION]
    transactions = db[TRANSACTION_COLLECTION]
    if block_height_db == 0:
        block_height_db = get_latest_block_on_db(db)+1
    if block_height_node == 0:
        block_height_node = get_latest_block_on_node(w3)
    print(block_height_db, block_height_node)
    for block_id in range(block_height_db, block_height_node+1):
        block = get_block_dict(w3, block_id)
        if block:
            block["totalDifficulty"] = str(block["totalDifficulty"])
            block["difficulty"] = str(block["difficulty"])
            try:
                blocks.insert_one(block)
                logging.info("success: {}".format(block_id))
            except Exception as e:
                logging.info(
                    "{} Block Insertion Failed {}".format(block_id, e))
            for transaction in block["transactions"]:
                transaction_id = transaction.hex()
                transaction_details = get_transaction_info(
                    w3, transaction.hex())
                if transaction_details:
                    transaction_details["value_wei"] = str(
                        transaction_details["value"])
                    transaction_details["value"] = transaction_details["value"] / \
                        pow(10, 18)
                    transaction_details["gas_wei"] = str(
                        transaction_details["gas"])
                    transaction_details["gas"] = transaction_details["gas"] / \
                        pow(10, 18)
                    transaction_details["gasPrice_wei"] = str(
                        transaction_details["gasPrice"])
                    transaction_details["gasPrice"] = transaction_details["gasPrice"] / pow(
                        10, 18)
                    transaction_details["timestamp"] = block["timestamp"]
                    try:
                        transactions.insert_one(transaction_details)
                        print("success: {}/{}".format(block_id, transaction_id))
                        logging.info(
                            "success: {}/{}".format(block_id, transaction_id))
                    except Exception as e:
                        logging.info(
                            "{} Transaction Insertion Failed {}".format(transaction_id, e))

                else:
                    logging.info("Transaction {}  {}".format(
                        transaction_id, "Failed"))
                    continue
        else:
            print("Block {} {}".format(block_id, "Failed"))
            logging.info("Block {} {}".format(block_id, "Failed"))
            continue
    executing_load = False
    mongoClient.close()
    print("Disconnected with DB")
    return


def get_latest_block_on_db(db_connection):
    try:
        result = list(db_connection.blocks.find(
            None, {"number": 1}).sort("number", -1).limit(1))
        return result[0]['number']
    except Exception as e:
        logging.error("Failed get latest block on DB{}".format(e))


def get_latest_block_on_node(w3):
    try:
        latest = w3.eth.getBlock('latest')['number']
        return latest
    except Exception as e:
        logging.error("Failed get latest block on Node {}".format(e))


def run_loop():
    while not executing_load:
        load_blocks()


run_loop()
