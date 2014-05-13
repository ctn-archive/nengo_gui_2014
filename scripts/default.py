import nengo

model = nengo.Network()
with model:
    a = nengo.Ensemble(n_neurons=80, dimensions=2, label="testasdfasdfasdfasfd")

    vis = nengo.Network(label="tester")
    with vis:
        b = nengo.Ensemble(n_neurons=80, dimensions=2)
        d = nengo.Ensemble(n_neurons=80, dimensions=2)

#       v1 = nengo.Network()
#       with v1:
#           c = nengo.Ensemble(n_neurons=80, dimensions=2)
    nengo.Connection(a,b)
    nengo.Connection(b,d)

import nengo_gui
gui = nengo_gui.Config()
gui[a].pos = 200, 100
gui[vis].pos = 200, 200
gui[b].pos = -40, 0 #relative to centre of network
gui[d].pos = 40, 0 #relative to centre of network
