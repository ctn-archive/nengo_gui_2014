import json
import re
import keyword

import random
import pprint

def isidentifier(s):
    if s in keyword.kwlist:
        return False
    return re.match(r'^[a-z_][a-z0-9_]*$', s, re.I) is not None


class Converter(object):
    def __init__(self, model, codelines):
        self.model = model
        self.codelines = codelines
        self.objects = []
        self.links = []
        self.object_index = {}
        self.process(model)

    def find_identifier(self, line, default):
        text = self.codelines[line]
        if '=' in text:
            text = text.split('=', 1)[0].strip()
            if isidentifier(text):
                return text
        return default

    def process(self, network, id_prefix=None):
        random.seed(3)
        for i, ens in enumerate(network.ensembles):
            line = ens._created_line_number-1
            label = ens.label
            if label == 'Ensemble':
                label = self.find_identifier(line, label)
            id = 'e%d' % i
            if id_prefix is not None:
                id = '%s.%s'%(id_prefix, id)


            obj = {'label':label, 'line':line, 'id':id, 'type':'ens',
                   'x':random.uniform(0,300), 'y':random.uniform(0,300)}
            self.object_index[ens] = len(self.objects)
            self.objects.append(obj)
        for i, nde in enumerate(network.nodes):
            line = nde._created_line_number-1
            label = nde.label
            if label == 'Node':
                label = self.find_identifier(line, label)
            id = 'd%d' % i
            if id_prefix is not None:
                id = '%s.%s'%(id_prefix, id)
            obj = {'label':label, 'line':line, 'id':id, 'type':'nde',
                   'x':random.uniform(0,300), 'y':random.uniform(0,300)}
            self.object_index[nde] = len(self.objects)
            self.objects.append(obj)
        for i, net in enumerate(network.networks):
            if not hasattr(net, '_created_line_number'):
                for obj in net.ensembles + net.nodes + net.connections:
                    net._created_line_number = obj._created_line_number
                    break
                else:
                    net._created_line_number = 0
            line = net._created_line_number-1
            label = net.label
            if label == 'Node':
                label = self.find_identifier(line, label)
            id = 'n%d' % i
            if id_prefix is not None:
                id = '%s.%s'%(id_prefix, id)

            self.process(net, id_prefix=id)

            contains = [self.object_index[obj] for obj in
                net.ensembles + net.nodes + net.networks]
            obj = {'label':label, 'line':line, 'id':id, 'type':'net',
                   'contains':contains,
                   'x':random.uniform(0,300), 'y':random.uniform(0,300)}
            self.object_index[net] = len(self.objects)
            self.objects.append(obj)


        for i, conn in enumerate(network.connections):
            id = 'c%d' % i
            if id_prefix is not None:
                id = '%s.%s'%(id_prefix, id)
            self.links.append({'source':self.object_index[conn.pre],
                               'target':self.object_index[conn.post],
                               'id':id,
                               'type':'std'})

    def to_json(self):
        data = dict(nodes=self.objects, links=self.links)
        pprint.pprint(data)
        return json.dumps(data)
