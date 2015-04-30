import nengo
from nengo.networks import BasalGanglia, Thalamus, EnsembleArray

import matplotlib.pyplot as plt
import numpy as np

model = nengo.Network(label="RL Network")
with model:
    num_choices = 3
    actions = [-1, 0, 1]
    
    def reward_func(t, x):
        reward = [0]*num_choices
        
        if t%1.0 > .9:
            user_choice = np.argmax(x[:num_choices])
            model_choice = np.argmax(x[num_choices:-1])
            
            user_action = actions[user_choice]
            model_action = x[-1]
            
            #reward[model_choice]= (1 if user_choice==model_choice else -1)
            reward[model_choice] = (1 if abs(user_action-model_action) <0.2
                else -1)

        return reward
    
    reward_input = nengo.Node(reward_func, size_in=2*num_choices+1, label="reward")
    user_input = nengo.Node([0]*num_choices, label="user")
    nengo.Connection(user_input, reward_input[:num_choices])
    
    state = nengo.Node([0], label="state")
    vals = nengo.Ensemble(300, 1, label='vals')
    
    nengo.Connection(state, vals)
    
    vals_relay = nengo.Node(size_in=num_choices, label='vals relay')
    err_conn = nengo.Connection(reward_input, vals_relay,
        modulatory=True)
    
    nengo.Connection(vals, vals_relay, function=lambda x: [0]*num_choices,
        learning_rule=nengo.PES(err_conn, 0.1))

    #nengo.Connection(vals_relay, reward_input[num_choices:])
    
    #Add a basal ganglia
    bg = BasalGanglia(num_choices, input_bias=.5, label="Basal Ganglia")
    nengo.Connection(vals_relay, bg.input)
    thalamus = Thalamus(num_choices, label="Thalamus")
    nengo.Connection(bg.output,thalamus.input)
    
    #select an action
    actions_node = nengo.Node(actions, label="actions")
    actions_array = EnsembleArray(50,num_choices, label="actions array")
    nengo.Connection(actions_node, actions_array.input)
    
    for i,e in enumerate(actions_array.ensembles):
        nengo.Connection(thalamus.output, e.neurons, 
            transform=[np.roll([0,-10,-10], i)]*e.n_neurons)
            
    nengo.Connection(actions_array.output, reward_input[-1],
        transform=[[1]*num_choices])
    
    nengo.Connection(thalamus.output, reward_input[num_choices:-1])
    
    nengo.Probe(vals_relay)
    nengo.Probe(reward_input)
    nengo.Probe(bg.output)
    nengo.Probe(thalamus.output)
    nengo.Probe(actions_array.output)
    

import nengo_gui
gui = nengo_gui.Config()
gui[model].scale = 0.2869036712045938
gui[model].offset = 90.73577650170978,184.27951222659522
gui[vals].pos = 175.000, 587.500
gui[vals].scale = 1.000
gui[reward_input].pos = 175.000, 512.500
gui[reward_input].scale = 1.000
gui[user_input].pos = 50.000, 475.000
gui[user_input].scale = 1.000
gui[state].pos = 50.000, 550.000
gui[state].scale = 1.000
gui[vals_relay].pos = 300.000, 550.000
gui[vals_relay].scale = 1.000
gui[actions_node].pos = 50.000, 625.000
gui[actions_node].scale = 1.000
gui[bg].pos = 1078.805, 550.000
gui[bg].scale = 1.000
gui[bg].size = 1287.609, 992.000
gui[bg.input].pos = 600.000, 550.000
gui[bg.input].scale = 1.000
gui[bg.output].pos = 1675.000, 550.000
gui[bg.output].scale = 1.000
gui[bg.bias_input].pos = 475.000, 550.000
gui[bg.bias_input].scale = 1.000
gui[bg.networks[0]].pos = 900.000, 225.000
gui[bg.networks[0]].scale = 1.000
gui[bg.networks[0]].size = 330.000, 230.000
gui[bg.networks[0].ea_ensembles[0]].pos = 900.000, 150.000
gui[bg.networks[0].ea_ensembles[0]].scale = 1.000
gui[bg.networks[0].ea_ensembles[1]].pos = 900.000, 225.000
gui[bg.networks[0].ea_ensembles[1]].scale = 1.000
gui[bg.networks[0].ea_ensembles[2]].pos = 900.000, 300.000
gui[bg.networks[0].ea_ensembles[2]].scale = 1.000
gui[bg.networks[0].input].pos = 775.000, 225.000
gui[bg.networks[0].input].scale = 1.000
gui[bg.networks[0].output].pos = 1025.000, 187.500
gui[bg.networks[0].output].scale = 1.000
gui[bg.networks[0].func_str].pos = 1025.000, 262.500
gui[bg.networks[0].func_str].scale = 1.000
gui[bg.networks[1]].pos = 900.000, 550.000
gui[bg.networks[1]].scale = 1.000
gui[bg.networks[1]].size = 330.000, 230.000
gui[bg.networks[1].ea_ensembles[0]].pos = 900.000, 475.000
gui[bg.networks[1].ea_ensembles[0]].scale = 1.000
gui[bg.networks[1].ea_ensembles[1]].pos = 900.000, 550.000
gui[bg.networks[1].ea_ensembles[1]].scale = 1.000
gui[bg.networks[1].ea_ensembles[2]].pos = 900.000, 625.000
gui[bg.networks[1].ea_ensembles[2]].scale = 1.000
gui[bg.networks[1].input].pos = 775.000, 550.000
gui[bg.networks[1].input].scale = 1.000
gui[bg.networks[1].output].pos = 1025.000, 512.500
gui[bg.networks[1].output].scale = 1.000
gui[bg.networks[1].func_str].pos = 1025.000, 587.500
gui[bg.networks[1].func_str].scale = 1.000
gui[bg.networks[2]].pos = 900.000, 875.000
gui[bg.networks[2]].scale = 1.000
gui[bg.networks[2]].size = 330.000, 230.000
gui[bg.networks[2].ea_ensembles[0]].pos = 900.000, 800.000
gui[bg.networks[2].ea_ensembles[0]].scale = 1.000
gui[bg.networks[2].ea_ensembles[1]].pos = 900.000, 875.000
gui[bg.networks[2].ea_ensembles[1]].scale = 1.000
gui[bg.networks[2].ea_ensembles[2]].pos = 900.000, 950.000
gui[bg.networks[2].ea_ensembles[2]].scale = 1.000
gui[bg.networks[2].input].pos = 775.000, 875.000
gui[bg.networks[2].input].scale = 1.000
gui[bg.networks[2].output].pos = 1025.000, 837.500
gui[bg.networks[2].output].scale = 1.000
gui[bg.networks[2].func_stn].pos = 1025.000, 912.500
gui[bg.networks[2].func_stn].scale = 1.000
gui[bg.networks[3]].pos = 1375.000, 387.500
gui[bg.networks[3]].scale = 1.000
gui[bg.networks[3]].size = 330.000, 230.000
gui[bg.networks[3].ea_ensembles[0]].pos = 1375.000, 312.500
gui[bg.networks[3].ea_ensembles[0]].scale = 1.000
gui[bg.networks[3].ea_ensembles[1]].pos = 1375.000, 387.500
gui[bg.networks[3].ea_ensembles[1]].scale = 1.000
gui[bg.networks[3].ea_ensembles[2]].pos = 1375.000, 462.500
gui[bg.networks[3].ea_ensembles[2]].scale = 1.000
gui[bg.networks[3].input].pos = 1250.000, 387.500
gui[bg.networks[3].input].scale = 1.000
gui[bg.networks[3].output].pos = 1500.000, 350.000
gui[bg.networks[3].output].scale = 1.000
gui[bg.networks[3].func_gpi].pos = 1500.000, 425.000
gui[bg.networks[3].func_gpi].scale = 1.000
gui[bg.networks[4]].pos = 1375.000, 712.500
gui[bg.networks[4]].scale = 1.000
gui[bg.networks[4]].size = 330.000, 230.000
gui[bg.networks[4].ea_ensembles[0]].pos = 1375.000, 637.500
gui[bg.networks[4].ea_ensembles[0]].scale = 1.000
gui[bg.networks[4].ea_ensembles[1]].pos = 1375.000, 712.500
gui[bg.networks[4].ea_ensembles[1]].scale = 1.000
gui[bg.networks[4].ea_ensembles[2]].pos = 1375.000, 787.500
gui[bg.networks[4].ea_ensembles[2]].scale = 1.000
gui[bg.networks[4].input].pos = 1250.000, 712.500
gui[bg.networks[4].input].scale = 1.000
gui[bg.networks[4].output].pos = 1500.000, 675.000
gui[bg.networks[4].output].scale = 1.000
gui[bg.networks[4].func_gpe].pos = 1500.000, 750.000
gui[bg.networks[4].func_gpe].scale = 1.000
gui[thalamus].pos = 2070.000, 387.500
gui[thalamus].scale = 1.000
gui[thalamus].size = 420.000, 417.000
gui[thalamus.bias].pos = 1900.000, 387.500
gui[thalamus.bias].scale = 1.000
gui[thalamus.actions].pos = 2137.500, 387.500
gui[thalamus.actions].scale = 1.000
gui[thalamus.actions].size = 205.000, 305.000
gui[thalamus.actions.ea_ensembles[0]].pos = 2075.000, 275.000
gui[thalamus.actions.ea_ensembles[0]].scale = 1.000
gui[thalamus.actions.ea_ensembles[1]].pos = 2075.000, 350.000
gui[thalamus.actions.ea_ensembles[1]].scale = 1.000
gui[thalamus.actions.ea_ensembles[2]].pos = 2075.000, 425.000
gui[thalamus.actions.ea_ensembles[2]].scale = 1.000
gui[thalamus.actions.input].pos = 2075.000, 500.000
gui[thalamus.actions.input].scale = 1.000
gui[thalamus.actions.output].pos = 2200.000, 387.500
gui[thalamus.actions.output].scale = 1.000
gui[actions_array].pos = 2075.000, 800.000
gui[actions_array].scale = 1.000
gui[actions_array].size = 330.000, 230.000
gui[actions_array.ea_ensembles[0]].pos = 2075.000, 725.000
gui[actions_array.ea_ensembles[0]].scale = 1.000
gui[actions_array.ea_ensembles[1]].pos = 2075.000, 800.000
gui[actions_array.ea_ensembles[1]].scale = 1.000
gui[e].pos = 2075.000, 875.000
gui[e].scale = 1.000
gui[actions_array.input].pos = 1950.000, 800.000
gui[actions_array.input].scale = 1.000
gui[actions_array.output].pos = 2200.000, 800.000
gui[actions_array.output].scale = 1.000
