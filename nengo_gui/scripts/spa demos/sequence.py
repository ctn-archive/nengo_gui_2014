import nengo
from nengo import spa

dimensions = 16  

class Sequence(spa.SPA):
    def __init__(self):            
        # Specify the modules to be used
        self.cortex = spa.Buffer(dimensions=dimensions)

        # Specify the action mapping
        self.actions = spa.Actions(
            'dot(cortex, A) --> cortex = B',
            'dot(cortex, B) --> cortex = C',
            'dot(cortex, C) --> cortex = D',
            'dot(cortex, D) --> cortex = E',
            'dot(cortex, E) --> cortex = A'
        )

        self.bg = spa.BasalGanglia(actions=self.actions)
        self.thal = spa.Thalamus(self.bg)

        self.input = spa.Input(cortex=lambda t: 'A' 
            if t<.05 else '0')
        
model = Sequence(label='Sequence_Module')

with model:
    state = nengo.Probe(model.cortex.state.output, synapse=0.01)
    actions = nengo.Probe(model.thal.actions.output, synapse=0.01)
    utility = nengo.Probe(model.bg.input, synapse=0.01)
    

import nengo_gui
gui = nengo_gui.Config()
gui[model].scale = 0.2484519992054184
gui[model].offset = 63.101416044725,113.87770651834754
gui[model.cortex].pos = 500.000, 775.000
gui[model.cortex].scale = 1.000
gui[model.cortex].size = 410.000, 192.000
gui[model.cortex.state].pos = 500.000, 775.000
gui[model.cortex.state].scale = 1.000
gui[model.cortex.state].size = 330.000, 80.000
gui[model.cortex.state.ea_ensembles[0]].pos = 500.000, 775.000
gui[model.cortex.state.ea_ensembles[0]].scale = 1.000
gui[model.cortex.state.input].pos = 375.000, 775.000
gui[model.cortex.state.input].scale = 1.000
gui[model.cortex.state.output].pos = 625.000, 775.000
gui[model.cortex.state.output].scale = 1.000
gui[model.thal.bg].pos = 2037.219, 775.000
gui[model.thal.bg].scale = 1.000
gui[model.thal.bg].size = 1204.438, 1442.000
gui[model.bg.input].pos = 1475.000, 737.500
gui[model.bg.input].scale = 1.000
gui[model.bg.output].pos = 2550.000, 775.000
gui[model.bg.output].scale = 1.000
gui[model.bg.bias].pos = 1475.000, 812.500
gui[model.bg.bias].scale = 1.000
gui[model.bg.networks[0]].pos = 1775.000, 300.000
gui[model.bg.networks[0]].scale = 1.000
gui[model.bg.networks[0]].size = 330.000, 380.000
gui[model.bg.networks[0].ea_ensembles[0]].pos = 1775.000, 150.000
gui[model.bg.networks[0].ea_ensembles[0]].scale = 1.000
gui[model.bg.networks[0].ea_ensembles[1]].pos = 1775.000, 225.000
gui[model.bg.networks[0].ea_ensembles[1]].scale = 1.000
gui[model.bg.networks[0].ea_ensembles[2]].pos = 1775.000, 300.000
gui[model.bg.networks[0].ea_ensembles[2]].scale = 1.000
gui[model.bg.networks[0].ea_ensembles[3]].pos = 1775.000, 375.000
gui[model.bg.networks[0].ea_ensembles[3]].scale = 1.000
gui[model.bg.networks[0].ea_ensembles[4]].pos = 1775.000, 450.000
gui[model.bg.networks[0].ea_ensembles[4]].scale = 1.000
gui[model.bg.networks[0].input].pos = 1650.000, 300.000
gui[model.bg.networks[0].input].scale = 1.000
gui[model.bg.networks[0].output].pos = 1900.000, 262.500
gui[model.bg.networks[0].output].scale = 1.000
gui[model.bg.networks[0].func_str].pos = 1900.000, 337.500
gui[model.bg.networks[0].func_str].scale = 1.000
gui[model.bg.networks[1]].pos = 1775.000, 775.000
gui[model.bg.networks[1]].scale = 1.000
gui[model.bg.networks[1]].size = 330.000, 380.000
gui[model.bg.networks[1].ea_ensembles[0]].pos = 1775.000, 625.000
gui[model.bg.networks[1].ea_ensembles[0]].scale = 1.000
gui[model.bg.networks[1].ea_ensembles[1]].pos = 1775.000, 700.000
gui[model.bg.networks[1].ea_ensembles[1]].scale = 1.000
gui[model.bg.networks[1].ea_ensembles[2]].pos = 1775.000, 775.000
gui[model.bg.networks[1].ea_ensembles[2]].scale = 1.000
gui[model.bg.networks[1].ea_ensembles[3]].pos = 1775.000, 850.000
gui[model.bg.networks[1].ea_ensembles[3]].scale = 1.000
gui[model.bg.networks[1].ea_ensembles[4]].pos = 1775.000, 925.000
gui[model.bg.networks[1].ea_ensembles[4]].scale = 1.000
gui[model.bg.networks[1].input].pos = 1650.000, 775.000
gui[model.bg.networks[1].input].scale = 1.000
gui[model.bg.networks[1].output].pos = 1900.000, 737.500
gui[model.bg.networks[1].output].scale = 1.000
gui[model.bg.networks[1].func_str].pos = 1900.000, 812.500
gui[model.bg.networks[1].func_str].scale = 1.000
gui[model.bg.networks[2]].pos = 1775.000, 1250.000
gui[model.bg.networks[2]].scale = 1.000
gui[model.bg.networks[2]].size = 330.000, 380.000
gui[model.bg.networks[2].ea_ensembles[0]].pos = 1775.000, 1100.000
gui[model.bg.networks[2].ea_ensembles[0]].scale = 1.000
gui[model.bg.networks[2].ea_ensembles[1]].pos = 1775.000, 1175.000
gui[model.bg.networks[2].ea_ensembles[1]].scale = 1.000
gui[model.bg.networks[2].ea_ensembles[2]].pos = 1775.000, 1250.000
gui[model.bg.networks[2].ea_ensembles[2]].scale = 1.000
gui[model.bg.networks[2].ea_ensembles[3]].pos = 1775.000, 1325.000
gui[model.bg.networks[2].ea_ensembles[3]].scale = 1.000
gui[model.bg.networks[2].ea_ensembles[4]].pos = 1775.000, 1400.000
gui[model.bg.networks[2].ea_ensembles[4]].scale = 1.000
gui[model.bg.networks[2].input].pos = 1650.000, 1250.000
gui[model.bg.networks[2].input].scale = 1.000
gui[model.bg.networks[2].output].pos = 1900.000, 1212.500
gui[model.bg.networks[2].output].scale = 1.000
gui[model.bg.networks[2].func_stn].pos = 1900.000, 1287.500
gui[model.bg.networks[2].func_stn].scale = 1.000
gui[model.bg.networks[3]].pos = 2250.000, 537.500
gui[model.bg.networks[3]].scale = 1.000
gui[model.bg.networks[3]].size = 330.000, 380.000
gui[model.bg.networks[3].ea_ensembles[0]].pos = 2250.000, 387.500
gui[model.bg.networks[3].ea_ensembles[0]].scale = 1.000
gui[model.bg.networks[3].ea_ensembles[1]].pos = 2250.000, 462.500
gui[model.bg.networks[3].ea_ensembles[1]].scale = 1.000
gui[model.bg.networks[3].ea_ensembles[2]].pos = 2250.000, 537.500
gui[model.bg.networks[3].ea_ensembles[2]].scale = 1.000
gui[model.bg.networks[3].ea_ensembles[3]].pos = 2250.000, 612.500
gui[model.bg.networks[3].ea_ensembles[3]].scale = 1.000
gui[model.bg.networks[3].ea_ensembles[4]].pos = 2250.000, 687.500
gui[model.bg.networks[3].ea_ensembles[4]].scale = 1.000
gui[model.bg.networks[3].input].pos = 2125.000, 537.500
gui[model.bg.networks[3].input].scale = 1.000
gui[model.bg.networks[3].output].pos = 2375.000, 500.000
gui[model.bg.networks[3].output].scale = 1.000
gui[model.bg.networks[3].func_gpi].pos = 2375.000, 575.000
gui[model.bg.networks[3].func_gpi].scale = 1.000
gui[model.bg.networks[4]].pos = 2250.000, 1012.500
gui[model.bg.networks[4]].scale = 1.000
gui[model.bg.networks[4]].size = 330.000, 380.000
gui[model.bg.networks[4].ea_ensembles[0]].pos = 2250.000, 862.500
gui[model.bg.networks[4].ea_ensembles[0]].scale = 1.000
gui[model.bg.networks[4].ea_ensembles[1]].pos = 2250.000, 937.500
gui[model.bg.networks[4].ea_ensembles[1]].scale = 1.000
gui[model.bg.networks[4].ea_ensembles[2]].pos = 2250.000, 1012.500
gui[model.bg.networks[4].ea_ensembles[2]].scale = 1.000
gui[model.bg.networks[4].ea_ensembles[3]].pos = 2250.000, 1087.500
gui[model.bg.networks[4].ea_ensembles[3]].scale = 1.000
gui[model.bg.networks[4].ea_ensembles[4]].pos = 2250.000, 1162.500
gui[model.bg.networks[4].ea_ensembles[4]].scale = 1.000
gui[model.bg.networks[4].input].pos = 2125.000, 1012.500
gui[model.bg.networks[4].input].scale = 1.000
gui[model.bg.networks[4].output].pos = 2375.000, 975.000
gui[model.bg.networks[4].output].scale = 1.000
gui[model.bg.networks[4].func_gpe].pos = 2375.000, 1050.000
gui[model.bg.networks[4].func_gpe].scale = 1.000
gui[model.thal].pos = 1070.000, 775.000
gui[model.thal].scale = 1.000
gui[model.thal].size = 420.000, 567.000
gui[model.thal.bias].pos = 900.000, 775.000
gui[model.thal.bias].scale = 1.000
gui[model.thal.actions].pos = 1137.500, 775.000
gui[model.thal.actions].scale = 1.000
gui[model.thal.actions].size = 205.000, 455.000
gui[model.thal.actions.ea_ensembles[0]].pos = 1075.000, 587.500
gui[model.thal.actions.ea_ensembles[0]].scale = 1.000
gui[model.thal.actions.ea_ensembles[1]].pos = 1075.000, 662.500
gui[model.thal.actions.ea_ensembles[1]].scale = 1.000
gui[model.thal.actions.ea_ensembles[2]].pos = 1075.000, 737.500
gui[model.thal.actions.ea_ensembles[2]].scale = 1.000
gui[model.thal.actions.ea_ensembles[3]].pos = 1075.000, 812.500
gui[model.thal.actions.ea_ensembles[3]].scale = 1.000
gui[model.thal.actions.ea_ensembles[4]].pos = 1075.000, 887.500
gui[model.thal.actions.ea_ensembles[4]].scale = 1.000
gui[model.thal.actions.input].pos = 1075.000, 962.500
gui[model.thal.actions.input].scale = 1.000
gui[model.thal.actions.output].pos = 1200.000, 775.000
gui[model.thal.actions.output].scale = 1.000
gui[model.input].pos = 100.000, 775.000
gui[model.input].scale = 1.000
gui[model.input].size = 80.000, 80.000
gui[model.input.nodes[0]].pos = 100.000, 775.000
gui[model.input.nodes[0]].scale = 1.000
