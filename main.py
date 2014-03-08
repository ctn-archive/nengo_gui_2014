"""Entry point for launching the Nengo GUI.

Usage: python main.py [port=8080]
"""

import tornado.ioloop
import tornado.web

import os.path
import traceback
import sys
import webbrowser

import nengo_helper
import nengo

import re
import keyword


def isidentifier(s):
    if s in keyword.kwlist:
        return False
    return re.match(r'^[a-z_][a-z0-9_]*$', s, re.I) is not None


class MainHandler(tornado.web.RequestHandler):
    """Request handler for the main landing page."""

    def get(self):
        self.render('index.html')


class ModelBuildingHandler(tornado.web.RequestHandler):
    """Request handler for building models."""

    def post(self):
        code = self.get_argument('code')
        code = code.replace('\r\n', '\n')
        self.write(self._build_model(code))

    def _build_model(self, code, filename='<string>'):
        try:
            c = compile(code, filename, 'exec')
            locals = {}
            globals = {}
            exec c in globals, locals

        except (SyntaxError, Exception):
            try:
                e_type, e_value, e_traceback = sys.exc_info()
                tb = traceback.extract_tb(e_traceback)

                if e_type is SyntaxError:
                    error_line = e_value.lineno
                elif e_type is IndentationError:
                    error_line = e_value.lineno
                else:
                    for (fn, line, funcname, text) in reversed(tb):
                        if fn == filename:
                            error_line = line
                            break
                    else:
                        print 'Unknown Error'
                        error_line = 0

                print tb
                traceback.print_exc()

                return dict(error_line=error_line, text=str(e_value))
            except:
                traceback.print_exc()

        try:
            model = locals['model']
            nodes = []
            node_map = {}
            links = []
            for obj in model.objs:
                node_map[obj] = len(nodes)

                label = obj.label
                if ((isinstance(obj, nengo.Ensemble) and label=='Ensemble') or
                      (isinstance(obj, nengo.Node) and label=='Node') or
                      (isinstance(obj, nengo.Network) and label=='Network')):

                    text = code.splitlines()[obj._created_line_number-1]
                    if '=' in text:
                        text = text.split('=', 1)[0].strip()
                        if isidentifier(text):
                            obj.label = text

                nodes.append(dict(label=obj.label, line=obj._created_line_number-1, id=len(nodes)))
            for c in model.connections:
                links.append(dict(source=node_map[c.pre], target=node_map[c.post], id=len(links)))
        except:
            traceback.print_exc()
            return dict(error_line=2, text='Unknown')

        return dict(nodes=nodes, links=links)


class Application(tornado.web.Application):
    """Main application class for holding global server state."""

    def initialize(self, **kwargs):
        # Set up globally accessible data-structures / etc in here!
        # They can be accessed in the request via self.application.
        pass


settings = {
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'debug': True,
}

application = Application([
    (r'/', MainHandler),
    (r'/build', ModelBuildingHandler),
], **settings)


if __name__ == '__main__':
    port = int((sys.argv + [8080])[1])
    application.listen(port)
    webbrowser.open_new_tab('http://localhost:%d/' % port)
    tornado.ioloop.IOLoop.instance().start()
