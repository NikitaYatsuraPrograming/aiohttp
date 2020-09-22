import aiopg.sa
from sqlalchemy import (MetaData,
                        Table,
                        Column,
                        ForeignKey,
                        Integer,
                        String,
                        Date, create_engine)

from aiohttpdemo_polls.settings import config

meta = MetaData()

# Создание таблицы
question = Table(
    'question', meta,

    Column('id', Integer, primary_key=True),
    Column('question_text', String(200), nullable=False),
    Column('pub_date', Date, nullable=False)
)

# Создание таблицы
choice = Table(
    'choice', meta,

    Column('id', Integer, primary_key=True),
    Column('choice_text', String(200), nullable=False),
    Column('votes', Integer, server_default='0', nullable=False),

    Column('question_id', Integer, ForeignKey('question.id', ondelete='CASCADE'))
)

DNS = "postgresql://{user}:{password}@{host}:{port}/{database}"
db_url = DNS.format(**config['postgres'])
engine = create_engine(db_url)
conn = engine.connect()


async def add_in_db_question(question_text, pub_date):
    conn.execute(question.insert(), [
        {'question_text': question_text,
         'pub_date': pub_date}
    ])


async def get_question(id_question):
    """
    Вывод информации по айди

    :param id_question:
    :return:
    """

    t = conn.execute(question.select().where(question.c.id == id_question))
    return t


async def update_question_in_db(id_question, question_text, pub_date):
    """
    Обновление

    :param id_question:
    :param question_text:
    :param pub_date:
    :return:
    """

    conn.execute(question.update().where(question.c.id == id_question).values(question_text=question_text,
                                                                              pub_date=pub_date))


async def delete_question_in_db(id_question):
    """
    Удаление

    :param id_question:
    :return:
    """

    conn.execute(question.delete().where(question.c.id == id_question))


async def init_pg(app):
    """
    Иницализация бд (все переменные берутся из config/polls.yaml)

    :param app:
    :return:
    """

    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
    )
    app['db'] = engine


async def close_pg(app):
    """
    Закрытие бд

    :param app:
    :return:
    """

    app['db'].close()
    await app['db'].wait_closed()
