import requests
import json
from config import currency


class APIException(Exception):
    pass


class CurrencyConvert:
    @staticmethod
    def get_price(base: str, qoute: str, amount: str):        
        try:
            base = currency[base]
        except KeyError:
            raise APIException(f'Неверно указана валюта {base}!')
        
        try:
            qoute = currency[qoute]
        except KeyError:
            raise APIException(f'Неверно указана валюта {qoute}!')
        
        try:
            amount = float(amount)
        except TypeError:
            raise APIException(f'Неверно указано количество {amount}')

        if base == qoute:
            raise APIException('Невозможно перевести одинаковые валюты!')


        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base}&tsyms={qoute}').content
        base_price = json.loads(r)[qoute]

        return float(base_price)
    