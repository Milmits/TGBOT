from decimal import Decimal
from urllib import response

import requests
from telebot import formatting
from telebot import TeleBot, types, util, formatting

import config

USD_BEL_RUB = 3.3

FAVORITE_CURRENCIES = ["USD", "EUR", "TRY", "BYN", "RUB", "PLN"]

DEFAULT_LOCAL_CURRENCY = "BYN"


