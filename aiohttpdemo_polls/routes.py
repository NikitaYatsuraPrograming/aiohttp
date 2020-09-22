from aiohttpdemo_polls.views import index, add_question, details_question, update_question, delete_question


def setup_routes(app):
    """
    URL адреса

    :param app:
    :return:
    """

    app.router.add_get('/', index, name='index')
    app.router.add_get('/add_question', add_question)
    app.router.add_post('/add_question', add_question)
    app.router.add_get(r'/{name:[0-9]}', details_question)
    app.router.add_get(r'/update/{name:[0-9]}', update_question)
    app.router.add_post(r'/update/{name:[0-9]}', update_question)
    app.router.add_get(r'/delete/{name:[0-9]}', delete_question)
    app.router.add_post(r'/delete/{name:[0-9]}', delete_question)
