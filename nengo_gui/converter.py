import json
import re
import keyword
import namefinder

import nengo
from nengo.vis.ipython import D3DataRenderer
from nengo.vis.modelgraph import ModelGraph


def isidentifier(s):
    if s in keyword.kwlist:
        return False
    return re.match(r'^[a-z_][a-z0-9_]*$', s, re.I) is not None


class NengoGuiRenderer(D3DataRenderer):
    def render_ensemble(self, ens):
        data = super(NengoGuiRenderer, self).render_ensemble(ens)
        data.update({'line': ens.nengo_object._created_line_number - 1})
        return data

    def render_node(self, node):
        data = super(NengoGuiRenderer, self).render_node(node)
        data.update({'line': node.nengo_object._created_line_number - 1})
        return data

    def render_network(self, net):
        data = super(NengoGuiRenderer, self).render_network(net)
        nengo_net = net.nengo_object
        if not hasattr(nengo_net, '_created_line_number'):
            children = (nengo_net.ensembles + nengo_net.nodes +
                        nengo_net.connections)
            for obj in children:
                nengo_net._created_line_number = obj._created_line_number
                break
            else:
                nengo_net._created_line_number = 0
        line = nengo_net._created_line_number-1
        data.update({'line': line})
        return data

    def render_collapsed_network(self, net):
        data = super(NengoGuiRenderer, self).render_collapsed_network(net)
        nengo_net = net.nengo_object
        if not hasattr(nengo_net, '_created_line_number'):
            children = (nengo_net.ensembles + nengo_net.nodes +
                        nengo_net.connections)
            for obj in children:
                nengo_net._created_line_number = obj._created_line_number
                break
            else:
                nengo_net._created_line_number = 0
        line = nengo_net._created_line_number-1
        data.update({'line': line})
        return data


class Converter(object):
    def __init__(self, model, codelines, locals, config):
        self.model = model
        self.namefinder = namefinder.NameFinder(locals, model)
        self.namefinder.find_names(self.model)
        self.codelines = codelines
        self.config = config
        self.modelgraph = ModelGraph(self.model)

    def to_json(self):
        renderer = NengoGuiRenderer(self.config, self.namefinder)
        return renderer.render(self.modelgraph)
