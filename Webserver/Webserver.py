import threading

from twisted.web.static import File
from twisted.internet import endpoints, reactor
from twisted.web.server import Site
from klein import Klein


class Webserver(threading.Thread):
    app = Klein()

    def __init__(self):
        threading.Thread.__init__(self)

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

    @app.route('/', branch=True)
    def static(self, request):

        return 'test'

