from sqlalchemy import create_engine, MetaData

from aiohttpdemo_polls.settings import config
from aiohttpdemo_polls.db import question, choice

# Путь который формирует settings
DNS = "postgresql://{user}:{password}@{host}:{port}/{database}"


def create_tables(engine):
    """
    Создание таблицы

    :param engine:
    :return:
    """

    meta = MetaData()
    meta.create_all(bind=engine, tables=[question, choice])


if __name__ == '__main__':
    db_url = DNS.format(**config['postgres'])
    engine = create_engine(db_url)

    create_tables(engine)
