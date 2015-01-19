import nengo
import numpy as np
from nengo.utils.functions import piecewise
from nengo.utils import distributions

## Import letter path data
files = ['a', 'c', 'p', 'nima', 'aaron', 'jon']
letter_to_draw = 'jon'
letters = {}

for letter in files:  #Paths extracted as velocities
    tmp=[]
    with open(letter+'.txt') as f:
        for line in f:
            tmp.append(line.strip().split(',') )
            
    tmp = np.array(tmp,dtype=float)
    tmp = (tmp-tmp[0,:]) #normalize to start at zero
    tmp[:,1]=-tmp[:,1]+1  #flip it right side up
    tmp = tmp/(np.max(tmp, axis=0)) #Normalize max width to 1; change for 't','h', etc.?

    letters[letter]=tmp
    
#Nengo network to learn how to draw feedforward 2 x 1D populations
N = 500 #Number of neurons
tau = .01 #time constant for connections
w = 6 #proportional to frequency

def samples(Ns):
    s = distributions.Uniform(0,np.pi*2)
    theta = s.sample(Ns)
    return np.concatenate([np.cos(theta)[:,None],np.sin(theta)[:,None]], axis=1)

model = nengo.Network(label='Handwriting')
with model:
    draw_pop = nengo.Ensemble(N, dimensions=2, radius = 1, label="Draw", 
                       intercepts=distributions.Uniform(0.8,1.1))
    
    osc_pop = nengo.Ensemble(N, dimensions=2, radius = 1, label="Oscillator", 
                       intercepts=distributions.Uniform(0.3,1.1))

    input1 = nengo.Node(output=lambda t: ([1,1] if t<.01 else [0,0]))
    
    output1 = nengo.Node(output=lambda t,x:x, size_in=2)

    nengo.Connection(input1, osc_pop, synapse=tau) 
    nengo.Connection(osc_pop, osc_pop, transform = [[1.1,w],[-1,1.1]], synapse = .1)
    nengo.Connection(osc_pop, draw_pop)

    # Define a function that returns the path
    def drawAx(x):
        x0,x1 = x
        xlet = np.array(letters[letter_to_draw][:,0])
        theta = np.arctan2(x1,x0)
        if theta<0: theta = theta+2*np.pi
        ind = int(np.floor((theta-1)*xlet.size/(2*np.pi-2)))
        if ind < 0: ind=0
        if ind >= xlet.size: ind = xlet.size-1

        xnew = xlet[ind]
        
        return xnew
    
    def drawAy(x):
        x0,x1 = x
        ylet = np.array(letters[letter_to_draw][:,1])
        theta = np.arctan2(x1,x0)
        if theta<0: theta = theta+2*np.pi
        ind = int(np.floor((theta-1)*ylet.size/(2*np.pi-2)))
        if ind < 0: ind=0
        if ind >= ylet.size: ind = ylet.size-1

        ynew = ylet[ind]
        
        return ynew

    nengo.Connection(draw_pop, output1, function=drawAx, transform=[[1],[0]], synapse=tau, eval_points=samples(5000))
    nengo.Connection(draw_pop, output1, function=drawAy, transform=[[0],[1]], synapse=tau, eval_points=samples(5000))

    in_probe = nengo.Probe(input1, 'output')
    out_probe = nengo.Probe(output1, 'output')
    draw_spikes = nengo.Probe(draw_pop, 'spikes')
    osc_prob = nengo.Probe(osc_pop)



import nengo_gui
gui = nengo_gui.Config()
gui[model].scale = 2.3586206896551727
gui[model].offset = -32.75862068965523,86.41122341813713
gui[draw_pop].pos = 196.623, 67.880
gui[draw_pop].scale = 1.000
gui[osc_pop].pos = 131.771, 68.929
gui[osc_pop].scale = 1.000
gui[input1].pos = 49.576, 69.693
gui[input1].scale = 1.000
gui[output1].pos = 265.234, 67.763
gui[output1].scale = 1.000
