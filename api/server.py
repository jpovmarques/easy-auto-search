import time
from bottle import route, run
from db_client import Database_client


class Server:
    db_client = Database_client()
    def __init__(self):
        run(host='localhost', port=1111)

    @route('/')
    def index():
        return {'path': 'home'}

    @route('/api/count')
    def count():
        return Server.db_client.count()

    @route('/api/all_cars')
    def all():
        return Server.db_client.all()

    @route('/api/status')
    def api_status():
    	return {'status': 'online', 'servertime': time.time()}
