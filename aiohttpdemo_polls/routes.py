from aiohttpdemo_polls.views import index


def setup_routes(app):
    """
    URL адреса

    :param app:
    :return:
    """

    app.router.add_get('/', index)
