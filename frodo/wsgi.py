import json
import logging
import frodo

db = frodo.plain()


class ObjID(object):
    def __eq__(self, other):
        return True


ROUTES = (
    (
        ('POST', ['containers', ObjID()]),
        lambda route, payload: {}
    )
)


def split_path(path):
    return path.strip('/').lower().split('/', 5)


def request_handler(method, route, env):

    for path in ROUTES:
        try:
            (r, f) = path
            m, p = r
            if (m == method and
                    all([c == route[i] for i, c in enumerate(p)]) and
                    all([c == p[i] for i, c in enumerate(route)])):
                return (
                    '200 OK' if method == 'GET' else '201 Created',
                    [('Content-Type', 'application/json')],
                    f(route, env['wsgi.input']),
                )
        except IndexError:  # when len(route) != len(p)
            continue

    return (
        '404 Not Found',
        [],
        None,
    )


def application(env, start_response):
    route = split_path(env['PATH_INFO'])
    method = env['REQUEST_METHOD']

    try:
        code, response_headers, body = request_handler(method, route, env)
    except Exception, e:
        logging.exception(e)
        code = '404 Not Found'
        response_headers = []
        body = None

    start_response(
        code,
        response_headers
    )
    return [json.dumps(body)] if body is not None else []
