import nengo_gui.swi
import os.path
import json
import traceback
import sys
from nengo_gui.feedforward_layout import feedforward_layout
import nengo_gui.converter
import nengo_gui.layout
import nengo_gui.nengo_helper
import nengo_gui.namefinder
import nengo
import os
try:
    from urllib import unquote
except ImportError:
    from urllib.parse import unquote

import threading

import nengo.spa

import nengo_gui
import pkgutil
import tempfile

import socket
try:
    import rpyc
    s = rpyc.classic.connect('localhost')
    assert s.modules.timeview.javaviz.__name__ == 'timeview.javaviz'
    import javaviz
    javaviz_message = 'run with JavaViz'
except ImportError:
    javaviz_message = 'JavaViz disabled as rpyc is not installed.'
    javaviz_message += ' Try "pip install rpyc"'
    javaviz = None
except socket.error:
    javaviz_message = 'JavaViz disabled as the javaviz server is not running'
    javaviz = None
except AssertionError:
    javaviz_message = 'JavaViz disabled due to an unknown server error.'
    javaviz_message += ' Please reinstall and re-run the JavaViz server'
    javaviz = None

try:
    import nengo_viz
    nengo_viz_message = 'Run model'
except ImportError:
    nengo_viz = None
    nengo_viz_message = 'nengo_viz not installed'




class NengoGui(nengo_gui.swi.SimpleWebInterface):
    default_filename = 'default.py'
    script_path = os.path.join(os.path.dirname(nengo_gui.__file__), 'scripts')
    refresh_interval = 0
    realtime_simulator = False
    simulator_class = nengo.Simulator
    nengo_viz_started = False


    def swi_static(self, *path):
        if self.user is None: return
        fn = os.path.join('static', *path)
        if fn.endswith('.js'):
            mimetype = 'text/javascript'
        elif fn.endswith('.css'):
            mimetype = 'text/css'
        elif fn.endswith('.png'):
            mimetype = 'image/png'
        elif fn.endswith('.gif'):
            mimetype = 'image/gif'
        else:
            raise Exception('unknown extenstion for %s' % fn)

        data = pkgutil.get_data('nengo_gui', fn)
        return (mimetype, data)

    def swi_favicon_ico(self):
        icon = pkgutil.get_data('nengo_gui', 'static/favicon.ico')
        return ('image/ico', icon)

    def swi(self):
        if self.user is None:
            return self.create_login_form()
        html = pkgutil.get_data('nengo_gui', 'templates/index.html')
        html = html.decode("utf-8")
        if javaviz is None:
            use_javaviz = 'false'
        else:
            use_javaviz = 'true'
        if nengo_viz is None:
            use_nengo_viz = 'false'
        else:
            use_nengo_viz = 'true'

        return html % dict(filename=self.default_filename,
                           refresh_interval=self.refresh_interval,
                           use_javaviz=use_javaviz,
                           use_nengo_viz=use_nengo_viz,
                           javaviz_message=javaviz_message,
                           nengo_viz_message=nengo_viz_message)

    def create_login_form(self):
        message = "Enter the password:"
        if self.attemptedLogin:
            message = "Invalid password"
        return """<form action="/" method="POST">%s<br/>
        <input type=hidden name=swi_id value="" />
        <input type=password name=swi_pwd>
        </form>""" % message

    @classmethod
    def set_default_filename(klass, fn):
        klass.default_filename = fn
        path, fn = os.path.split(fn)
        klass.script_path = path
        klass.default_filename = fn

    @classmethod
    def set_simulator_class(klass, simulator_class):
        """Which Simulator to use"""
        klass.simulator_class = simulator_class

    @classmethod
    def set_realtime_simulator_mode(klass, realtime_simulator):
        """Flag whether GUI should be in real-time mode"""
        klass.realtime_simulator = realtime_simulator

    @classmethod
    def set_refresh_interval(klass, interval):
        klass.refresh_interval = interval

    def swi_browse(self, dir):
        if self.user is None: return
        r = ['<ul class="jqueryFileTree" style="display: none;">']
        # r.append('<li class="directory collapsed"><a href="#" rel="../">..</a></li>')
        d = unquote(dir)
        for f in sorted(os.listdir(os.path.join(self.script_path, d))):
            ff = os.path.relpath(os.path.join(self.script_path, d,f), self.script_path)
            if os.path.isdir(os.path.join(self.script_path, d, ff)):
                r.append('<li class="directory collapsed"><a href="#" rel="%s/">%s</a></li>' % (ff,f))
            else:
                e = os.path.splitext(f)[1][1:] # get .ext and remove dot
                if e == 'py':
                    r.append('<li class="file ext_%s"><a href="#" rel="%s">%s</a></li>' % (e,ff,f))
        r.append('</ul>')
        return ''.join(r)

    def swi_openfile(self, filename):
        if self.user is None: return
        fn = os.path.join(self.script_path, filename)
        try:
            with open(fn, 'r') as f:
                text = f.read()
            # make sure there are no tabs in the file, since the editor is
            # supposed to use spaces instead
            text = text.replace('\t', '    ')
            modified_time = os.stat(fn).st_mtime
        except:
            text = ''
            modified_time = None
        return json.dumps(dict(text=text, mtime=modified_time))


    def swi_savefile(self, filename, code):
        if self.user is None: return
        fn = os.path.join(self.script_path, filename)
        with open(fn, 'w') as f:
            f.write(code.replace('\r\n', '\n'))
        return 'success'

    def swi_modified_time(self, filename):
        if self.user is None: return
        fn = os.path.join(self.script_path, filename)
        return repr(os.stat(fn).st_mtime)

    def swi_javaviz(self, filename, code):
        if self.user is None: return
        code = code.replace('\r\n', '\n')

        locals = {}
        exec(code, locals)

        model = locals['model']
        cfg = locals.get('gui', None)
        if cfg is None:
            cfg = nengo_gui.Config()

        model_config = locals.get('config', None)


        nf = nengo_gui.namefinder.NameFinder(locals, model)

        jv = javaviz.View(model, default_labels=nf.known_name,
                          filename=filename, realtime=self.realtime_simulator)
        if model_config is not None:
            sim = self.simulator_class(model, config=model_config)
        else:
            sim = self.simulator_class(model)
        jv.update_model(sim)
        jv.view(config=cfg)
        try:
            if self.realtime_simulator:
                sim.run()
            else:
                while True:
                    try:
                        sim.run(1)
                    except javaviz.VisualizerResetException:
                        sim.reset()
        except javaviz.VisualizerExitException:
            print('Finished running JavaViz simulation')

    def swi_nengo_viz(self, filename, code):
        if self.user is None: return
        code = code.replace('\r\n', '\n')
        fn = os.path.join(self.script_path, filename)

        locals = {}
        exec(code, locals)

        model = locals['model']

        viz = nengo_viz.Viz(filename=fn, model=model, locals=locals)
        nengo_viz.server.Server.viz = viz

        port = 8080

        if not self.nengo_viz_started:
            t = threading.Thread(target=nengo_viz.server.Server.start,
                             kwargs=dict(port=port, browser=False))
            t.daemon = True
            t.start()
            self.nengo_viz_started = True

        return '%d' % port


    def swi_graph_json(self, code, feedforward=False, graph_mode='normal'):
        if self.user is None: return
        if feedforward == "true":
            feedforward = True
        code = code.replace('\r\n', '\n')

        try:
            index = code.index('\nimport nengo_gui\n')
            code_gui = code[index:]
            code = code[:index]
        except ValueError:
            code_gui = ''

        codefile, code_fn = tempfile.mkstemp(suffix='nengo_gui_temp.py')
        with os.fdopen(codefile, 'w') as f:
            f.write(code)

        try:
            c = compile(code, code_fn, 'exec')
            locals = {}
            exec(c, locals)
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
                        if fn == code_fn:
                            error_line = line
                            break
                    else:
                        print('Unknown Error')
                        error_line = 0

                print(tb)
                traceback.print_exc()

                os.remove(code_fn)

                return json.dumps(dict(error_line=error_line, text=str(e_value)))
            except:
                traceback.print_exc()
        os.remove(code_fn)

        # run gui code lines, skipping ones that cause name errors
        for i, line in enumerate(code_gui.splitlines()):
            try:
                exec(line, globals(), locals)
            except NameError:
                # this is generally caused by having a gui[x].pos statement
                #  for something that has been deleted
                pass
            except AttributeError:
                # this is generally caused by having a gui[a.x].pos statement
                #  for something that has been deleted
                pass
            except IndexError:
                # this is generally caused by having a statement like
                # gui[model.ensemble[i]].pos statement for something that has
                # been deleted
                pass
            except KeyError:
                # this is generally caused by having a gui[input].pos statement
                #  for something that has been deleted but happened to have
                #  the same name as a builtin
                pass

        model = locals.get('model', None)
        if model is None:
            return json.dumps(dict(error_line=1,
                text='The top-level nengo.Network must be named "model"'))

        if graph_mode == 'normal':
            if feedforward:
                cfg = nengo_gui.Config()

                conv = nengo_gui.converter.Converter(model, code.splitlines(), locals, cfg)
                feedforward_layout(model, cfg, locals, conv.links, conv.objects)
                conv.global_scale = 1.0
                conv.global_offset = 0.0, 0.0
            else:
                cfg = locals.get('gui', None)
                if cfg is None:
                    cfg = nengo_gui.Config()

                gui_layout = nengo_gui.layout.Layout(model, cfg)
                conv = nengo_gui.converter.Converter(model, code.splitlines(), locals, cfg)

            return conv.to_json()
        else:
            return json.dumps(dict(nodes=[], links=[],
                                   global_scale=1.0, global_offset=(0,0)))
