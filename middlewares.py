import aiohttp_jinja2
from aiohttp import web


async def handle_404(request):
    """
    Обработка 404 ошибки

    :param request:
    :return:
    """
    return aiohttp_jinja2.render_template('404.html', request, {})


async def handle_500(request):
    """
    Обработка 500 ошибки

    :param request:
    :return:
    """
    return aiohttp_jinja2.render_template('500.html', request, {})


def create_error_middleware(overrides):
    """
    Создание обработчика

    :param overrides:
    :return:
    """

    @web.middleware
    async def error_middleware(request, handler):
        """
        Отлавливание ошибок которые могут возникнуть в ходе выполнения

        :param request:
        :param handler:
        :return:
        """

        try:
            response = await handler(request)

            override = overrides.get(response.status)
            if override:
                return await handler(request)

            return response

        except web.HTTPException as ex:
            override = overrides.get(ex.status)

            if override:
                return await override(request)

            raise

    return error_middleware


def setup_middlewares(app):
    """
    Запуск определенного обработчика

    :param app:
    :return:
    """

    error_middleware = create_error_middleware({
        404: handle_404,
        500: handle_500,
    })

    app.middlewares.append(error_middleware)
