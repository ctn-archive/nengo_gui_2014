"""Handlers for responding to all HTTP requests."""

import tornado.ioloop
import tornado.web
from tornado import gen

import nengo

import json
import logging
import sys
import traceback

import util


class MainHandler(tornado.web.RequestHandler):
    """Request handler for the main landing page."""

    def get(self):
        self.render('index.html')


class ModelHandler(tornado.web.RequestHandler):
    """Request handler for displaying models."""

    def get(self):
        code = self.get_argument('code')
        self.write(self._serialize_model(code))

    @classmethod
    def get_model(cls, code, filename='<string>'):
        c = compile(code.replace('\r\n', '\n'), filename, 'exec')
        locals = {}
        globals = {}
        exec c in globals, locals
        return locals['model']

    @classmethod
    def _serialize_model(cls, code, filename='<string>'):
        try:
            model = cls.get_model(code)

        except:
            e_type, e_value, e_traceback = sys.exc_info()
            tb = traceback.extract_tb(e_traceback)

            if e_type is SyntaxError:
                error_line = e_value.lineno
            elif e_type is IndentationError:
                error_line = e_value.lineno
            else:
                for fn, line, funcname, text in reversed(tb):
                    if fn == filename:
                        error_line = line
                        break
                else:
                    logging.warn('Unknown Error: %s', tb)
                    error_line = 0

            logging.debug(util.traceback_exc())
            return {'error_line': error_line, 'text': str(e_value)}

        nodes = []
        node_map = {}
        links = []
        lines = code.splitlines()
        for obj in model.objs:
            node_map[obj] = len(nodes)

            label = obj.label
            if (isinstance(obj, nengo.Ensemble) and label == 'Ensemble') or \
               (isinstance(obj, nengo.Node) and label == 'Node') or \
               (isinstance(obj, nengo.Network) and label == 'Network'):
                text = lines[obj._created_line_number-1]
                if '=' in text:
                    text = text.split('=', 1)[0].strip()
                    if util.is_identifier(text):
                        obj.label = text

            nodes.append({
                'label': obj.label,
                'line': obj._created_line_number-1,
                'id': len(nodes),
            })

        for c in model.connections:
            if not isinstance(c.post, nengo.Probe):
                links.append({
                    'source': node_map[c.pre],
                    'target': node_map[c.post],
                    'id': len(links),
                })

        return {'nodes': nodes, 'links': links}


class SimulationHandler(tornado.web.RequestHandler):
    """Request handler for streaming simulation data."""

    _simulators = {
        None: nengo.Simulator,
    }
    _default_dt = 0.001

    def prepare(self):
        """Callback for when the connection is opened."""
        self._is_closed = False

    @tornado.web.asynchronous
    @gen.engine
    def get(self):
        """Asynchronously streams the simulation data."""
        # Get the user-specified code and simulation parameters
        code = self.get_argument('code')
        sim = self.get_argument('sim', None)
        dt = float(self.get_argument('dt', self._default_dt))

        # Build the model and simulator
        model = ModelHandler.get_model(code)
        simulator = self._simulators[sim](model, dt)

        # Maintain an active connection, blocking only during each step
        while not self._is_closed:
            data = yield gen.Task(self._step, simulator)
            logging.debug('Connection (%d): %s', id(self), data)
            response = json.dumps(data)
            self.write('%d;%s;' % (len(response), response))
            self.flush()

    def _step(self, simulator, callback):
        """Advances the simulator one step, and then invokes callback(data)."""
        simulator.step()
        probes = {}
        for probe in simulator.model.probemap:
            probes[probe.label] = list(simulator.data(probe)[-1])
        data = {
            't': simulator.n_steps * simulator.model.dt,
            'probes': probes,
        }
        # Return control to the main IOLoop in order to process any other
        # pending requests, before re-entering the yield point in the coroutine
        tornado.ioloop.IOLoop.instance().add_callback(lambda: callback(data))

    def on_connection_close(self):
        """Callback for when the active connection is closed."""
        self._is_closed = True
