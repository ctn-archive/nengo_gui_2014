import nengo

model = nengo.Network()
with model:
    a = nengo.Ensemble(n_neurons=80, dimensions=2)

    vis = nengo.Network()
    with vis:
        b = nengo.Ensemble(n_neurons=80, dimensions=2)

        v1 = nengo.Network()
        with v1:
            c = nengo.Ensemble(n_neurons=80, dimensions=2)
            d = nengo.Ensemble(n_neurons=80, dimensions=2)
            nengo.Connection(c, d)

        nengo.Connection(b, c)

    nengo.Connection(a, b)