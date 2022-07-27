import yaml
import telebot as tl
import sqlite3
from pathlib import Path
from src.adapter import SQLAdapter


def read_yaml(path: str):
    with open(f"{path}.yml", "r", encoding="utf-8") as _file:
        return yaml.full_load(_file)


ROOT = Path(__file__).parent.parent
CONFIG = read_yaml(rf"{ROOT}\config")

SETUP, QUERIES, TEXT = CONFIG["setup"], CONFIG["query"], CONFIG["text"]
DATABASE = SETUP["connection"]["database"]
TOKEN = SETUP["token"]

# CONNECTION_OLD = sqlite3.connect(DATABASE, check_same_thread=False)
CONNECTION = SQLAdapter(sqlite3.connect, database=DATABASE, check_same_thread=False)
bot = tl.TeleBot(TOKEN)
