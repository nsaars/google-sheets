from asyncio import sleep
from db.models import Order
from sheets.sheets import SheetsAuthorizer, Table
from data.config import auth_creds_file, MAILING_TIME, FROM_TABLE, TO_TABLE
from datetime import datetime
from cb_api.currency import CurrencyRu
from telegram_bot.notify_admins import notify_admins
from telegram_bot.loader import dp


async def main():
    account = SheetsAuthorizer(auth_creds_file)
    service = await account.get_service()
    from_table = Table(service, FROM_TABLE)
    to_table = Table(service, TO_TABLE)
    ru_currency = CurrencyRu()

    while True:
        from_table_values = (await from_table.read(start_ceil='A', end_ceil='D'))[
            'values']  # getting values from source table
        await to_table.write(from_table_values, start_ceil='A', end_ceil='D')  # setting new values into own table
        await Controller.update_db(to_table, ru_currency)  # updating db
        print('database was update successfully', datetime.now().strftime("%d.%m.%Y %H:%M:%S"))

        await sleep(50)


async def notify_outdated():
    while True:
        if datetime.now().strftime("%H:%M") == MAILING_TIME:
            outdated_delivery = await Order.query.where(Order.delivery_time < datetime.today()).gino.all()
            outdated_messages = [f'Order {d.order_number} with delivery time: {d.delivery_time}.' for d in
                                 outdated_delivery]

            message = "The delivery period for the following products is overdue:\n\n" + '\n'.join(outdated_messages)
            if outdated_messages:
                await notify_admins(dp, message)
            await sleep(10)
        await sleep(50)


class Controller:

    @staticmethod
    async def __delete_outdated(sheet_values: list):
        orders = await Order.query.gino.all()
        sheet_ids = {int(t[0]) for t in sheet_values}
        order_ids = {order.id for order in orders}
        delete_ids = order_ids - sheet_ids

        await Order.delete.where(Order.id.in_(delete_ids)).gino.status()

    @staticmethod
    async def __update_outdated(sheet_values_dict: dict, ru_currency: CurrencyRu):
        orders = await Order.query.gino.all()
        for order in orders:
            if int(sheet_values_dict[order.id][0]) != order.order_number:
                order_number = int(sheet_values_dict[order.id][0])
                await order.update(order_number=order_number).apply()
            if int(sheet_values_dict[order.id][1]) != order.price:
                price = int(sheet_values_dict[order.id][1])
                await order.update(price=price).apply()
                ruble_price = await ru_currency.get_currency_price(price)
                await order.update(ruble_price=ruble_price).apply()
            if sheet_values_dict[order.id][2] != order.delivery_time.strftime('%d.%m.%Y'):
                await order.update(delivery_time=datetime.strptime(sheet_values_dict[order.id][2], '%d.%m.%Y')).apply()

    @staticmethod
    async def __append_new_values(sheet_values: list, ru_currency: CurrencyRu):
        orders = await Order.query.gino.all()
        sheet_ids = {int(t[0]) for t in sheet_values}
        order_ids = {order.id for order in orders}
        append_ids = sheet_ids - order_ids

        append_rows = (t for t in sheet_values if int(t[0]) in append_ids)

        for row in append_rows:
            ruble_price = await ru_currency.get_currency_price(int(row[2]))
            delivery_time = datetime.strptime(row[3], '%d.%m.%Y')
            await Order.create(id=int(row[0]), order_number=int(row[1]), price=int(row[2]),
                               delivery_time=delivery_time, ruble_price=ruble_price)

    @staticmethod
    async def update_ruble_price(sheet: Table):
        values = [['стоимость,₽']] + [list(ruble_price) for ruble_price in await Order.select('ruble_price').gino.all()]
        await sheet.write(values, start_ceil='E', end_ceil='E')

    @staticmethod
    async def update_db(sheet: Table, ru_currency: CurrencyRu):
        sheet_values = (await sheet.read(start_ceil='A', end_ceil='D'))['values'][1:]
        sheet_values_dict = {int(row[0]): row[1:] for row in sheet_values}

        await Controller.__delete_outdated(sheet_values)
        await Controller.__update_outdated(sheet_values_dict, ru_currency)
        await Controller.__append_new_values(sheet_values, ru_currency)
        await Controller.update_ruble_price(sheet)
