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
    def search_with_pagination():
        try:
            page_size = int(request.query.page_size)
            page_number = int(request.query.page_number)
            if page_size and page_number:
                brand = request.query.brand or ''
                model = request.query.model or ''
                price_min = request.query.price_min or 0
                price_max = request.query.price_max or 0
                year_min = request.query.year_min or 0
                year_max = request.query.year_max or 0
                print('brand', repr(brand))
                print('model', repr(model))
                print('price_min', repr(price_min))
                print('price_max', repr(price_max))
                print('year_min', repr(year_min))
                print('year_max', repr(year_max))
                return Server.db_client.search(
                    int(page_size),
                    int(page_number),
                    str(brand),
                    str(model),
                    int(price_min),
                    int(price_max),
                    int(year_min),
                    int(year_max),
                )
            else:
                return {'error': 'page size and page number are required params'}
        except ValueError:
            return {'error': 'invalid format for params'}
