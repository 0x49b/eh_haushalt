import threading

from twisted.web.static import File
from twisted.internet import endpoints, reactor
from twisted.web.server import Site
from klein import Klein
import RPi.GPIO as GPIO
import json


class Webserver(threading.Thread):
    app = Klein()

    def __init__(self, id, data, stats):
        threading.Thread.__init__(self)

        self.id = id
        self.data = data
        self.stats = stats


    def run(self):
        # self.app.run("localhost", 8080)
        # Create desired endpoint
        endpoint_description = "tcp:port=8888"
        endpoint = endpoints.serverFromString(reactor, endpoint_description)

        # This actually starts listening on the endpoint with the Klein app
        endpoint.listen(Site(self.app.resource()))

        # After doing other things like setting up logging,
        # starting other services in the reactor or
        # listening on other ports or sockets:
        reactor.run(installSignalHandlers=False)

    def stop(self):
        self._Thread__stop()

    @app.route('/')
    def pg_root(self, request):
        return 'I am the root page!'

    """
    Create new asset
    """

    @app.route('/asset', methods=['POST'])
    def post_asset(self, request):
        print 'POST'

        asset = json.loads(request.content.read())
        asset['id'] = self.data[-1]['id'] + 1
        self.data.append(asset)

        self.set_headers(request)

        return json.dumps(asset)

    """
    Get all assets
    """
    @app.route('/asset')
    def get_assets(self, request):
        print 'GET'

        self.set_headers(request)

        return json.dumps(self.data)

    """
    Update asset
    """
    @app.route('/asset/<int:id>', methods=['PUT'])
    def put_asset(self, request, id):
        print 'PUT'

        obj = None
        asset = json.loads(request.content.read())
        print asset

        self.set_asset(asset, id, True)

        self.set_headers(request)

        return json.dumps(self.data)

    """
    Delete asset
    """
    @app.route('/asset/<int:id>', methods=['DELETE'])
    def delete_asset(self, request, id):
        print 'DELETE'

        index = None

        for object in self.data:
            if object['id'] == id:
                index = self.data.index(object)

        if index is not None:
            del self.data[index]

        self.set_headers(request)

        return json.dumps(self.data)

    """
    Get specific asset
    """
    @app.route('/asset/<int:id>')
    def get_asset(self, request, id):
        print 'GET'

        obj = None

        for object in self.data:
            if object['id'] == id:
                obj = object

        self.set_headers(request)

        return json.dumps(obj)

    """
    Get stats
    """
    @app.route('/stats')
    def get_stats(self, request):

        self.set_headers(request)

        return json.dumps(self.stats)

    def set_headers(self, request):
        request.setHeader('Content-Type', 'application/json')
        request.setHeader('Access-Control-Allow-Origin', '*')
        request.setHeader('Access-Control-Allow-Methods', 'GET')
        request.setHeader('Access-Control-Allow-Headers', 'x-prototype-version,x-requested-with')
        request.setHeader('Access-Control-Max-Age', 2520)

    def set_stats(self, stats):
        self.stats = stats

    def get_stats(self):
        return self.stats

    def set_assets(self, assets):
        for asset in assets:
            self.set_asset(asset, asset['id'], False)

    def set_asset(self, asset, id, setall):
        obj = None

        for object in self.data:
            if object['id'] == id:
                obj = object

        if obj is not None:
            if obj['status'] != asset['status']:
                obj['status'] = asset['status']
                GPIO.output(obj['gpio'], asset['status'])

            if setall:
                obj['name'] = asset['name']
                obj['times'] = asset['times']

    def get_assets(self):
        return self.data