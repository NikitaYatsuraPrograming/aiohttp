import aiohttp_jinja2

from aiohttpdemo_polls import db


# Декоратор шаблонизатора
@aiohttp_jinja2.template('index.html')
async def index(request):
    """
    Создание начальной странички

    :param request:
    :return:
    """
    async with request.app['db'].acquire() as conn:
        """
        Чтение записей из бд(таблица questions)
        """
        cursor = await conn.execute(db.question.select())
        records = await cursor.fetchall()
        questions = [dict(q) for q in records]
        return {"questions": questions}

