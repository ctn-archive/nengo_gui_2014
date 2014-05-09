import nengo

model = nengo.Network()
with model:
    a = nengo.Ensemble(n_neurons=100, dimensions=2, label='int')
    b = nengo.Ensemble(n_neurons=80, dimensions=2, label='wait')
    c = nengo.Ensemble(n_neurons=80, dimensions=2)
    d = nengo.Ensemble(n_neurons=80, dimensions=2)
    e = nengo.networks.EnsembleArray(80,2, label="array")

    vis = nengo.Network(label="vision")
    with vis:

		v1 = nengo.Network(label="primary")
		with v1:
			f = nengo.Ensemble(n_neurons=80, dimensions=2)
			g = nengo.Ensemble(n_neurons=80, dimensions=2)
			nengo.Connection(f, g)
			nengo.Connection(f, f)
			
		r = nengo.Ensemble(n_neurons=80, dimensions=2)
		t = nengo.Ensemble(n_neurons=80, dimensions=2)
		nengo.Connection(r, t)

    nengo.Connection(a, a, synapse = 0.01)
    nengo.Connection(a, b, synapse=0.01)
    nengo.Connection(b, c, synapse=0.01)
    nengo.Connection(c, d, synapse=0.01)
    nengo.Connection(c, r, synapse=0.01)
    nengo.Connection(b, d, synapse=0.01)
    nengo.Connection(d, e.input[:2], synapse=0.01)
