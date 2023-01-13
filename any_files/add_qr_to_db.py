import asyncio
from openpyxl import Workbook

from database.sqlite import DataBase
db = DataBase('tg.db')


async def test():
    await db.add_new_qr_code_to_db('123123')


asyncio.run(test())
