from datetime import datetime
from requests import get

from xmltodict import parse


class CurrencyRu:
    API_URL = 'http://www.cbr.ru/scripts/XML_daily.asp'

    async def get_currency(self, currency=None, date=None, round_up_to=None):
        if currency is None:
            currency = 'USD'
        if date is None:
            date = datetime.today()
        if round_up_to is None:
            round_up_to = 0

        request_url = f'{self.API_URL}?date_req={date.strftime("%d/%m/%Y")}'
        response = parse(get(request_url).text)

        for c in response['ValCurs']['Valute']:
            if c['CharCode'] == currency:
                return round(float(c['Value'].replace(',', '.')), round_up_to)

    async def get_all_currency(self, date=None, round_up_to=None):
        if date is None:
            date = datetime.today()
        if round_up_to is None:
            round_up_to = 0

        request_url = f'{self.API_URL}?date_req={date.strftime("%d/%m/%Y")}'
        response = parse(get(request_url).text)

        return {c['CharCode']: round(float(c['Value'].replace(',', '.')), round_up_to) for c in response['ValCurs']['Valute']}

    async def get_currency_price(self, value, currency=None, date=None):
        return value * await self.get_currency(currency, date)
