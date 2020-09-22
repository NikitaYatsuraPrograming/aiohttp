import datetime
import json

import aiohttp_jinja2
from aiohttp import web

from aiohttpdemo_polls import db

from aiohttpdemo_polls.db import add_in_db_question, get_question, update_question_in_db, delete_question_in_db


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

        def default(o):
            if isinstance(o, (datetime.date, datetime.datetime)):
                return o.isoformat()

        j = json.dumps(questions, sort_keys=True, indent=1, default=default)
        return web.json_response(j)


@aiohttp_jinja2.template('add_question.html')
async def add_question(request):
    """
    Страница добовления вопросов

    :param request:
    :return:
    """

    # print(request.query_string)
    form = request.query_string.split('&')
    d = {}
    for i in form:
        t = i.split('=')
        d[t[0]] = t[1]

    if request.method == 'POST':
        # form = await request.post()
        question_text = d['question_text']
        pub_date = d['pub_date']
        await add_in_db_question(question_text, pub_date)
        location = request.app.router['index'].url_for()
        raise web.HTTPFound(location=location)
    return {}


async def details_question(request):
    """
    Вывод всей информации по айди с таблицы question

    :param request:
    :return:
    """

    id_question = request.match_info['name']
    result = await get_question(id_question)
    result = result.fetchone()

    j = {
        'id': result[0],
        'question_text': result[1],
        'pub_date': result[2]
    }

    def default(o):
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()

    j = json.dumps(j, sort_keys=True, indent=1, default=default)
    return web.json_response(j)


async def update_question(request):
    """
    Обновдение информации в таблице question по айди

    :param request:
    :return:
    """
    id_question = request.match_info['name']

    form = request.query_string.split('&')
    d = {}
    for i in form:
        t = i.split('=')
        d[t[0]] = t[1]

    if request.method == 'POST':
        # form = await request.post()
        question_text = d['question_text']
        pub_date = d['pub_date']
        await update_question_in_db(id_question, question_text, pub_date)
        raise web.HTTPFound('/')
    else:
        id_question = request.match_info['name']
        result = await get_question(id_question)
        result = result.fetchone()

        j = {
            'id': result[0],
            'question_text': result[1],
            'pub_date': result[2]
        }

        def default(o):
            if isinstance(o, (datetime.date, datetime.datetime)):
                return o.isoformat()

        j = json.dumps(j, sort_keys=True, indent=1, default=default)
        return web.json_response(j)


@aiohttp_jinja2.template('delete.html')
async def delete_question(request):
    """
    Удаление записей из таблицы question по айди

    :param request:
    :return:
    """
    if request.method == 'POST':
        id_question = request.match_info['name']
        await delete_question_in_db(id_question)
        raise web.HTTPFound('/')

    else:
        return {}
