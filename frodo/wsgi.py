import json
import frodo

db = frodo.plain()


def split_path(path):
    return path.strip('/').lower().split('/', 5)


def request_handler(method, route, env):
    payload = json.loads(env['wsgi.input'].getvalue())

    return (
        '200 OK',
        [('Content-Type', 'text/html')],
        '',
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
