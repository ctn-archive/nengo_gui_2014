"""Entry point for launching the Nengo GUI.

Usage: python main.py [port=8080]
"""

import tornado.ioloop
import tornado.web

import logging
import os.path
import sys
import webbrowser

import nengo_helper
from handlers import MainHandler, ModelHandler, SimulationHandler


class Application(tornado.web.Application):
    """Main application class for holding global server state."""

    def __init__(self, *args, **kwargs):
        nengo_helper.initialize()

        # Set up globally accessible data-structures / etc in here!
        # They can be accessed in the request via self.application.

        # Set up logging
        level = logging.DEBUG if kwargs['debug'] else logging.WARNING
        logging.root.setLevel(level)

        super(Application, self).__init__(*args, **kwargs)


settings = {
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'debug': True,
}

application = Application([
    (r'/', MainHandler),
    (r'/model', ModelHandler),
    (r'/simulate', SimulationHandler),
], **settings)


if __name__ == '__main__':
    port = int((sys.argv + [8080])[1])
    application.listen(port)
    webbrowser.open_new_tab('http://localhost:%d/' % port)
    tornado.ioloop.IOLoop.instance().start()
