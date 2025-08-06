from core.protocols.http import HTTPRequest, HTTPResponse

def index(request):
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    return HTTPResponse.html(200, content)

def post_index(request):
    return HTTPResponse.json(200, {"message": "post_index"})

def not_found(request=None):
    with open('templates/404.html', 'r', encoding='utf-8') as f:
        content = f.read()

    return HTTPResponse.html(404, content)

def bad_request(request=None):
    with open('templates/400.html', 'r', encoding='utf-8') as f:
        content = f.read()

    return HTTPResponse.html(400, content)

routes = {
    ('GET', '/'): index,
    ('POST', '/'): post_index
}