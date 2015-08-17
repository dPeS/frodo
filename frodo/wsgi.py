import json
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
    for r, f in ROUTES:
        m, p = r
        if m == method and all([a == b for a, b in zip(p, route)]):
            body = f(route, env['wsgi.input'])

    return (
        '200 OK',
        [('Content-Type', 'text/html')],
        body,
    )


def application(env, start_response):
    route = split_path(env['PATH_INFO'])
    method = env['REQUEST_METHOD']

    code, response_headers, body = request_handler(method, route, env)

    start_response(
        code,
        response_headers
    )
    return [json.dumps(body)]
