import numpy as np

import nengo
from nengo.utils.distributions import Uniform, UniformHypersphere


class HeteroAssociative(nengo.Network):
    """Store (key, value) associations, and lookup the value by key."""

    def __init__(self, n_neurons, max_capacity, d_key, d_value, 
                 default_value=None, voja_learning_rate=0.5, 
                 pes_learning_rate=0.5, n_error=200, n_dopamine=50, 
                 dopamine_strength=20):
        # Set the default_value to 0 if unspecified
        if default_value is None:
            default_value = [0]*d_value

        # Create input and output passthrough nodes
        self.key = nengo.Node(size_in=d_key, label="key")
        self.value = nengo.Node(size_in=d_value, label="value")
        self.learning = nengo.Node(size_in=1, label="learning")
        self.output = nengo.Node(size_in=d_value, label="output")
        self.has_key = nengo.Node(size_in=1, label="has_key")

        # Create node/ensembles for scaling the learning rate
        self.dopamine = nengo.Ensemble(
            n_dopamine, 1, intercepts=Uniform(0.5, 1.0),
            encoders=[[1]]*n_dopamine, label="dopamine")
        self.nopamine = nengo.Ensemble(n_dopamine, 1, label="nopamine")

        # Create ensemble which acts as the dictionary. The encoders will
        # shift towards the keys with Voja's rule, and the decoders will
        # shift towards the values with the PES learning rule. Aim to have
        # (neurons.n_neurons / max_capacity) neurons fire for a random x.
        intercept = self.calculate_intercept(d_key, 1.0 / max_capacity)
        encoders = UniformHypersphere(d_key, surface=True).sample(n_neurons)
        
        self.memory = nengo.Ensemble(
            n_neurons, d_key, encoders=encoders,
            intercepts=[intercept]*n_neurons, label="memory")
        
        # Create the ensembles for calculating error * learning
        self.value_error = nengo.Ensemble(n_error, d_value, label="value_error")
        self.has_key_error = nengo.Ensemble(n_error, 1, label="has_key_error")
        value_conn = nengo.Connection(self.value_error, self.output, modulatory=True)
        has_key_conn = nengo.Connection(self.has_key_error, self.has_key, modulatory=True)

        
        # Connect the memory Ensemble to the output Node with PES(value_error)
        # and the has_key node with PES(has_key_error)
        # Use the encoders as the evaluation points
        self.value_pes = nengo.PES(
            value_conn, learning_rate=pes_learning_rate, label="learn_value")
        nengo.Connection(
            self.memory, self.output, eval_points=encoders, function=lambda x: default_value,
            synapse=None, learning_rule=self.value_pes)
        self.has_key_pes = nengo.PES(
            has_key_conn, learning_rate=pes_learning_rate, label="learn_has_key")
        nengo.Connection(
            self.memory, self.has_key, eval_points=encoders, function=lambda x: 0,
            synapse=None, learning_rule=self.has_key_pes)

        # Connect the learning signal to the error populations
        nengo.Connection(self.learning, self.dopamine, synapse=None)
        nengo.Connection(nengo.Node(output=[1], label="bias_nopamine"), self.nopamine)
        self._inhibit(self.dopamine, self.nopamine, amount=dopamine_strength)
        self._inhibit(self.nopamine, self.value_error, amount=dopamine_strength)
        self._inhibit(self.nopamine, self.has_key_error, amount=dopamine_strength)

        # Connect the key Node to the memory Ensemble with voja's rule
        self.voja = nengo.Voja(
            learning_rate=voja_learning_rate, learning=self.dopamine,
            label="learn_key")
        nengo.Connection(
            self.key, self.memory, synapse=None, learning_rule=self.voja)

        # Compute the value_error and has_key_error
        nengo.Connection(self.value, self.value_error, synapse=None)
        nengo.Connection(self.output, self.value_error, transform=-1)
        
        nengo.Connection(nengo.Node(output=[1], label="bias_error"), self.has_key_error)
        nengo.Connection(self.has_key, self.has_key_error, transform=-1)

    @classmethod
    def calculate_intercept(cls, d, p):
        """Returns c such that np.dot(u, v) >= c with probability p.

        Here, u and v are two randomly generated vectors of dimension d.
        This works by the following formula, (1 - x**2)**((d - 3)/2.0), which
        gives the probability that a coordinate of a random point on a
        hypersphere is equal to x.

        The probability distribution of the dot product of two randomly chosen
        vectors is equivalent to the above, since we can always rotate the
        sphere such that one of the vectors is a unit vector, and then the
        dot product just becomes the component corresponding to that unit
        vector.

        This can be used to find the intercept such that a randomly generated
        encoder will fire in response to a random input x with probability p.
        """
        x, cpx = cls._component_probability_dist(d)
        return x[cpx >= 1 - p][0]

    @classmethod
    def calculate_max_capacity(cls, d, c):
        """Calculates what max_capacity should be to achieve desired intercept.

        This is the inverse of _calculate_intercept. Given some number of
        dimensions d, returns the max_capacity such that
        _calculate_intercepts(d, 1.0 / max_capacity) == c.
        """
        x, cpx = cls._component_probability_dist(d)
        return 1.0 / (1 - cpx[x >= c][0])

    @classmethod
    def _component_probability_dist(cls, d, dx=0.001):
        """Returns x and py such that probability of component <= x is cpx."""
        x = np.arange(-1+dx, 1, dx)
        cpx = ((1 - x**2)**((d - 3)/2.0)).cumsum()
        cpx = cpx / sum(cpx) / dx
        return x, cpx

    @classmethod
    def _inhibit(cls, pre, post, amount, **kwargs):
        """Creates a connection which inhibits post whenever pre fires."""
        return nengo.Connection(
            pre.neurons, post.neurons,
            transform=-amount*np.ones((post.n_neurons, pre.n_neurons)),
            **kwargs)


# Configure Vocabulary
num_items = 5
d_key = 8
d_value = 1

np.random.seed(42)
keys = UniformHypersphere(d_key, surface=True).sample(num_items)
values = UniformHypersphere(d_value, surface=False).sample(num_items)


# Configure Test Input Functions
def iterate_periodically(l, period):
    return lambda t: l[(t/period) % len(l)]

period = 1.0

input_keys = iterate_periodically(keys, period)
input_values = iterate_periodically(values, period)
input_learning = lambda t: int(t < num_items*period - 0.1)


# Create the Model!
model = nengo.Network()
with model:
    associative = HeteroAssociative(1000, 5*num_items, d_key, d_value)
    key = nengo.Node(input_keys, label="input_key")
    value = nengo.Node(input_values, label="input_value")
    learning = nengo.Node(input_learning, label="input_learning")
    
    nengo.Connection(key, associative.key)
    nengo.Connection(value, associative.value)
    nengo.Connection(learning, associative.learning)
    
    nengo.Probe(associative.key)
    nengo.Probe(associative.value)
    nengo.Probe(associative.learning)
    
    nengo.Probe(associative.output)
    nengo.Probe(associative.has_key)
    nengo.Probe(associative.value_error)
    nengo.Probe(associative.has_key_error)


import nengo_gui
gui = nengo_gui.Config()
gui[model].scale = 0.9401509751835828
gui[model].offset = 13.544654153612193,8.725535825125164
gui[key].pos = 50.000, 175.000
gui[key].scale = 1.000
gui[value].pos = 50.000, 250.000
gui[value].scale = 1.000
gui[learning].pos = 50.000, 325.000
gui[learning].scale = 1.000
gui[associative].pos = 408.158, 276.796
gui[associative].scale = 1.000
gui[associative].size = 544.316, 412.000
gui[associative.dopamine].pos = 315.219, 257.796
gui[associative.dopamine].scale = 1.000
gui[associative.nopamine].pos = 372.826, 329.182
gui[associative.nopamine].scale = 1.000
gui[associative.memory].pos = 456.190, 147.000
gui[associative.memory].scale = 1.000
gui[associative.value_error].pos = 459.121, 250.425
gui[associative.value_error].scale = 1.000
gui[associative.has_key_error].pos = 487.902, 357.182
gui[associative.has_key_error].scale = 1.000
gui[associative.key].pos = 225.000, 126.796
gui[associative.key].scale = 1.000
gui[associative.value].pos = 225.000, 201.796
gui[associative.value].scale = 1.000
gui[associative.learning].pos = 225.000, 276.796
gui[associative.learning].scale = 1.000
gui[associative.output].pos = 623.864, 195.984
gui[associative.output].scale = 1.000
gui[associative.has_key].pos = 617.910, 344.424
gui[associative.has_key].scale = 1.000
gui[associative.nodes[5]].pos = 225.000, 351.796
gui[associative.nodes[5]].scale = 1.000
gui[associative.nodes[6]].pos = 225.000, 426.796
gui[associative.nodes[6]].scale = 1.000
