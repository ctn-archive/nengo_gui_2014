import nengo

model = nengo.Network('Demo Network')

with model:
    a = nengo.Ensemble(200,2, label='a', radius=1.4)
    b = nengo.Ensemble(200,1, label='b')
    
    def product(x):
        return x[0] * x[1]
    
    nengo.Connection(a,a[0],function=product, synapse=.1)
    
    input = nengo.Node([0,0])
    
    nengo.Connection(input,a)
    
    nengo.Probe(a)
    nengo.Probe(a, 'spikes')
    nengo.Probe(b)
    nengo.Probe(b, 'spikes')

import nengo_gui
gui = nengo_gui.Config()
gui[model].scale = 2.3810062657634696
gui[model].offset = -33.430187972903695,176.44968671182664
gui[a].pos = 175.000, 50.000
gui[a].scale = 1.000
gui[b].pos = 300.000, 50.000
gui[b].scale = 1.000
gui[input].pos = 50.000, 50.000
gui[input].scale = 1.000
