import time
from bottle import route, run, request
from db_client import Database_client


class Server:
    db_client = Database_client()
    def __init__(self):
        run(host='localhost', port=1111, reloader=True)

    @route('/')
    def index():
        return {'path': 'home'}

    @route('/api/status')
    def api_status():
        return {'status': 'online', 'servertime': time.time()}

    @route('/api/count')
    def count():
        return Server.db_client.count()

    @route('/api/all_cars')
    def all():
        return Server.db_client.all()

    @route('/api/search')
    def all_with_pagination():
        page_size = int(request.query.size)
        page_number = int(request.query.number)
        brand = request.query.brand or None
        return Server.db_client.search(page_size, page_number, brand)
