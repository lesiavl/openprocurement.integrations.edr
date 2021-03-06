import unittest
import os
import webtest
from gevent import monkey; monkey.patch_all()
from gevent.pywsgi import WSGIServer
from bottle import Bottle
from openprocurement.integrations.edr.utils import ROUTE_PREFIX


class PrefixedRequestClass(webtest.app.TestRequest):

    @classmethod
    def blank(cls, path, *args, **kwargs):
        path = '{0}{1}'.format(ROUTE_PREFIX, path)
        return webtest.app.TestRequest.blank(path, *args, **kwargs)


class BaseWebTest(unittest.TestCase):

    """Base Web Test to test openprocurement.integrations.edr. """

    relative_to = os.path.dirname(__file__)  # crafty line

    @classmethod
    def setUpClass(cls):
        cls.edr_api_app = Bottle()
        # setup_routing(cls.edr_api_app)
        cls.server = WSGIServer(('localhost', 20603), cls.edr_api_app, log=None)
        cls.server.start()
        for _ in range(10):
            try:
                cls.app = webtest.TestApp("config:tests.ini", relative_to=cls.relative_to)
            except:
                pass
            else:
                break
        else:
            cls.app = webtest.TestApp("config:tests.ini", relative_to=cls.relative_to)
        cls.app.RequestClass = PrefixedRequestClass

    @classmethod
    def tearDownClass(cls):
        cls.server.close()

    def setUp(self):
        self.app.authorization = ('Basic', ('robot', 'robot'))

    def tearDown(self):
        pass
