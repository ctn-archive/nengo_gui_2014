import nengo

model = nengo.Network()
with model:
    a = nengo.Ensemble(n_neurons=80, dimensions=2, label="testasdfasdfasdfasfd")

    b = nengo.Ensemble(n_neurons=80, dimensions=2)

    c = nengo.Ensemble(n_neurons=80, dimensions=2)
    
    v1=nengo.Network(label="V1")
    with v1:
        d = nengo.Ensemble(n_neurons=80, dimensions=2)
        e = nengo.Ensemble(n_neurons=80, dimensions=2)

    nengo.Connection(a,b)
    nengo.Connection(a,a)
    nengo.Connection(c,b)
    nengo.Connection(c,e)
    nengo.Connection(e,d)

import nengo_gui
gui = nengo_gui.Config()
gui[a].pos = 200, 100
gui[b].pos = 100, 200
gui[c].pos = 300, 200
