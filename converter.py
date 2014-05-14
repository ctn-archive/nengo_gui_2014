import json
import re
import keyword
import namefinder

import random
import pprint

def isidentifier(s):
    if s in keyword.kwlist:
        return False
    return re.match(r'^[a-z_][a-z0-9_]*$', s, re.I) is not None


class Converter(object):
    def __init__(self, model, codelines, locals, config):
        self.model = model
        self.namefinder = namefinder.NameFinder(locals, model)
        self.codelines = codelines
        self.objects = []
        self.config = config
        self.links = []
        self.object_index = {model:-1}
        self.process(model)

    def find_identifier(self, line, default):
        text = self.codelines[line]
        if '=' in text:
            text = text.split('=', 1)[0].strip()
            if isidentifier(text):
                return text
        return default

    def process(self, network, id_prefix=None):
        random.seed(5)
        
        for i, ens in enumerate(network.ensembles):
            line = ens._created_line_number-1
            label = ens.label
            if label == 'Ensemble':
                label = self.find_identifier(line, label)
            id = self.namefinder.name(ens)

            pos = self.config[ens].pos
            if pos is None:
                pos = random.uniform(0, 300), random.uniform(0, 300)
            obj = {'label':label, 'line':line, 'id':id, 'type':'ens',
                   'x':pos[0], 'y':pos[1], 'contained_by': self.object_index[network]}
            self.object_index[ens] = len(self.objects)
            self.objects.append(obj)
            
        for i, nde in enumerate(network.nodes):
            line = nde._created_line_number-1
            label = nde.label
            if label == 'Node':
                label = self.find_identifier(line, label)
            id = self.namefinder.name(nde)
            pos = self.config[nde].pos
            if pos is None:
                pos = random.uniform(0, 300), random.uniform(0, 300)
            obj = {'label':label, 'line':line, 'id':id, 'type':'nde',
                   'x':pos[0], 'y':pos[1], 'contained_by': self.object_index[network]}
            self.object_index[nde] = len(self.objects)
            self.objects.append(obj)
            
        full_contains={}
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
            id = self.namefinder.name(net)

            pos = self.config[net].pos
            if pos is None:
                pos = random.uniform(0, 300), random.uniform(0, 300)
            
            self.object_index[net] = len(self.objects)
            self.objects.append({'placeholder':0}) # place holder
            full_contains[i] = self.process(net, id_prefix=id)

            contains = [self.object_index[obj] for obj in
                net.ensembles + net.nodes + net.networks]
            
            full_contains[i] += contains
            
            obj = {'label':label, 'line':line, 'id':id, 'type':'net',
                   'contains':list(contains), 'full_contains': list(full_contains[i]),
                   'contained_by': self.object_index[network], 'x':pos[0], 'y':pos[1]}
            self.objects[self.object_index[net]] = obj


        for i, conn in enumerate(network.connections):
            id = self.namefinder.name(conn)
            self.links.append({'source':self.object_index[conn.pre],
                               'target':self.object_index[conn.post],
                               'id':id,
                               'type':'std'})
                               
        return sum(full_contains.values(),[])

    def to_json(self):
        if not hasattr(self.model, '_created_line_number'):
            for obj in self.model.ensembles + self.model.nodes + self.model.connections:
                self.model._created_line_number = obj._created_line_number
                break
            else:
                self.model._created_line_number = 0
        line = self.model._created_line_number-1
        label = self.model.label
        if label == 'Node':
            label = self.find_identifier(line, label)
        id = self.namefinder.name(self.model)
        contains = [self.object_index[obj] for obj in
                self.model.ensembles + self.model.nodes + self.model.networks]
        obj = {'label':label, 'line':line, 'id':id, 'type':'mod',
                   'contains':list(contains), 'contained_by': -1}
        self.objects.append(obj)
        
        data = dict(nodes=self.objects, links=self.links)
        pprint.pprint(data)
        return json.dumps(data)
