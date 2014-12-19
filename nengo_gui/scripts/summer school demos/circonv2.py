import nengo
import nengo.spa as spa

D = 16
N = 500

model = spa.SPA(label="circular convolution")
with model:
    
    vocab=spa.Vocabulary(D)
    vocab.parse('BLUE')
    
    a = nengo.Ensemble(N, D)
    b = nengo.Ensemble(N, D)
    c = nengo.Ensemble(N, D)
    d = nengo.Ensemble(N, D)
    e = nengo.Ensemble(N, D)
    
    model.config[a].vocab=vocab
    model.config[b].vocab=vocab

    circonv = nengo.networks.CircularConvolution(100, D)

    circonv2 = nengo.networks.CircularConvolution(100, D, invert_b=True)
    
    nengo.Connection(a, circonv.A)
    nengo.Connection(b, circonv.B)
    nengo.Connection(circonv.output, d)
    nengo.Connection(d, circonv2.A)
    nengo.Connection(c, circonv2.B)
    nengo.Connection(circonv2.output, e)
    
    nengo.Probe(a)
    nengo.Probe(b)
    nengo.Probe(c)
    nengo.Probe(d)
    nengo.Probe(e)
    


import nengo_gui
gui = nengo_gui.Config()
gui[model].scale = 0.08882685506825898
gui[model].offset = 372.942148452509,39.530495024661064
gui[a].pos = 50.000, 2937.500
gui[a].scale = 1.000
gui[b].pos = 50.000, 3012.500
gui[b].scale = 1.000
gui[c].pos = 50.000, 3087.500
gui[c].scale = 1.000
gui[d].pos = 1225.000, 3012.500
gui[d].scale = 1.000
gui[e].pos = 1350.000, 3012.500
gui[e].scale = 1.000
gui[circonv].pos = 637.500, 1512.500
gui[circonv].scale = 1.000
gui[circonv].size = 905.000, 2897.000
gui[circonv.A].pos = 225.000, 1475.000
gui[circonv.A].scale = 1.000
gui[circonv.B].pos = 225.000, 1550.000
gui[circonv.B].scale = 1.000
gui[circonv.output].pos = 1050.000, 1512.500
gui[circonv.output].scale = 1.000
gui[circonv.product].pos = 632.500, 1512.500
gui[circonv.product].scale = 1.000
gui[circonv.product].size = 545.000, 2785.000
gui[circonv.product.A].pos = 400.000, 1437.500
gui[circonv.product.A].scale = 1.000
gui[circonv.product.B].pos = 400.000, 1512.500
gui[circonv.product.B].scale = 1.000
gui[model.all_nodes[5]].pos = 400.000, 1587.500
gui[model.all_nodes[5]].scale = 1.000
gui[circonv.product.product].pos = 700.000, 1512.500
gui[circonv.product.product].scale = 1.000
gui[circonv.product.product].size = 330.000, 2705.000
gui[model.all_ensembles[5]].pos = 700.000, 200.000
gui[model.all_ensembles[5]].scale = 1.000
gui[model.all_ensembles[6]].pos = 700.000, 275.000
gui[model.all_ensembles[6]].scale = 1.000
gui[model.all_ensembles[7]].pos = 700.000, 350.000
gui[model.all_ensembles[7]].scale = 1.000
gui[model.all_ensembles[8]].pos = 700.000, 425.000
gui[model.all_ensembles[8]].scale = 1.000
gui[model.all_ensembles[9]].pos = 700.000, 500.000
gui[model.all_ensembles[9]].scale = 1.000
gui[model.all_ensembles[10]].pos = 700.000, 575.000
gui[model.all_ensembles[10]].scale = 1.000
gui[model.all_ensembles[11]].pos = 700.000, 650.000
gui[model.all_ensembles[11]].scale = 1.000
gui[model.all_ensembles[12]].pos = 700.000, 725.000
gui[model.all_ensembles[12]].scale = 1.000
gui[model.all_ensembles[13]].pos = 700.000, 800.000
gui[model.all_ensembles[13]].scale = 1.000
gui[model.all_ensembles[14]].pos = 700.000, 875.000
gui[model.all_ensembles[14]].scale = 1.000
gui[model.all_ensembles[15]].pos = 700.000, 950.000
gui[model.all_ensembles[15]].scale = 1.000
gui[model.all_ensembles[16]].pos = 700.000, 1025.000
gui[model.all_ensembles[16]].scale = 1.000
gui[model.all_ensembles[17]].pos = 700.000, 1100.000
gui[model.all_ensembles[17]].scale = 1.000
gui[model.all_ensembles[18]].pos = 700.000, 1175.000
gui[model.all_ensembles[18]].scale = 1.000
gui[model.all_ensembles[19]].pos = 700.000, 1250.000
gui[model.all_ensembles[19]].scale = 1.000
gui[model.all_ensembles[20]].pos = 700.000, 1325.000
gui[model.all_ensembles[20]].scale = 1.000
gui[model.all_ensembles[21]].pos = 700.000, 1400.000
gui[model.all_ensembles[21]].scale = 1.000
gui[model.all_ensembles[22]].pos = 700.000, 1475.000
gui[model.all_ensembles[22]].scale = 1.000
gui[model.all_ensembles[23]].pos = 700.000, 1550.000
gui[model.all_ensembles[23]].scale = 1.000
gui[model.all_ensembles[24]].pos = 700.000, 1625.000
gui[model.all_ensembles[24]].scale = 1.000
gui[model.all_ensembles[25]].pos = 700.000, 1700.000
gui[model.all_ensembles[25]].scale = 1.000
gui[model.all_ensembles[26]].pos = 700.000, 1775.000
gui[model.all_ensembles[26]].scale = 1.000
gui[model.all_ensembles[27]].pos = 700.000, 1850.000
gui[model.all_ensembles[27]].scale = 1.000
gui[model.all_ensembles[28]].pos = 700.000, 1925.000
gui[model.all_ensembles[28]].scale = 1.000
gui[model.all_ensembles[29]].pos = 700.000, 2000.000
gui[model.all_ensembles[29]].scale = 1.000
gui[model.all_ensembles[30]].pos = 700.000, 2075.000
gui[model.all_ensembles[30]].scale = 1.000
gui[model.all_ensembles[31]].pos = 700.000, 2150.000
gui[model.all_ensembles[31]].scale = 1.000
gui[model.all_ensembles[32]].pos = 700.000, 2225.000
gui[model.all_ensembles[32]].scale = 1.000
gui[model.all_ensembles[33]].pos = 700.000, 2300.000
gui[model.all_ensembles[33]].scale = 1.000
gui[model.all_ensembles[34]].pos = 700.000, 2375.000
gui[model.all_ensembles[34]].scale = 1.000
gui[model.all_ensembles[35]].pos = 700.000, 2450.000
gui[model.all_ensembles[35]].scale = 1.000
gui[model.all_ensembles[36]].pos = 700.000, 2525.000
gui[model.all_ensembles[36]].scale = 1.000
gui[model.all_ensembles[37]].pos = 700.000, 2600.000
gui[model.all_ensembles[37]].scale = 1.000
gui[model.all_ensembles[38]].pos = 700.000, 2675.000
gui[model.all_ensembles[38]].scale = 1.000
gui[model.all_ensembles[39]].pos = 700.000, 2750.000
gui[model.all_ensembles[39]].scale = 1.000
gui[model.all_ensembles[40]].pos = 700.000, 2825.000
gui[model.all_ensembles[40]].scale = 1.000
gui[circonv.product.product.input].pos = 575.000, 1512.500
gui[circonv.product.product.input].scale = 1.000
gui[circonv.product.product.output].pos = 825.000, 1475.000
gui[circonv.product.product.output].scale = 1.000
gui[circonv.product.product.product].pos = 825.000, 1550.000
gui[circonv.product.product.product].scale = 1.000
gui[circonv2].pos = 637.500, 4512.500
gui[circonv2].scale = 1.000
gui[circonv2].size = 905.000, 2897.000
gui[circonv2.A].pos = 225.000, 4475.000
gui[circonv2.A].scale = 1.000
gui[circonv2.B].pos = 225.000, 4550.000
gui[circonv2.B].scale = 1.000
gui[circonv2.output].pos = 1050.000, 4512.500
gui[circonv2.output].scale = 1.000
gui[circonv2.product].pos = 632.500, 4512.500
gui[circonv2.product].scale = 1.000
gui[circonv2.product].size = 545.000, 2785.000
gui[circonv2.product.A].pos = 400.000, 4437.500
gui[circonv2.product.A].scale = 1.000
gui[circonv2.product.B].pos = 400.000, 4512.500
gui[circonv2.product.B].scale = 1.000
gui[model.all_nodes[14]].pos = 400.000, 4587.500
gui[model.all_nodes[14]].scale = 1.000
gui[circonv2.product.product].pos = 700.000, 4512.500
gui[circonv2.product.product].scale = 1.000
gui[circonv2.product.product].size = 330.000, 2705.000
gui[model.all_ensembles[41]].pos = 700.000, 3200.000
gui[model.all_ensembles[41]].scale = 1.000
gui[model.all_ensembles[42]].pos = 700.000, 3275.000
gui[model.all_ensembles[42]].scale = 1.000
gui[model.all_ensembles[43]].pos = 700.000, 3350.000
gui[model.all_ensembles[43]].scale = 1.000
gui[model.all_ensembles[44]].pos = 700.000, 3425.000
gui[model.all_ensembles[44]].scale = 1.000
gui[model.all_ensembles[45]].pos = 700.000, 3500.000
gui[model.all_ensembles[45]].scale = 1.000
gui[model.all_ensembles[46]].pos = 700.000, 3575.000
gui[model.all_ensembles[46]].scale = 1.000
gui[model.all_ensembles[47]].pos = 700.000, 3650.000
gui[model.all_ensembles[47]].scale = 1.000
gui[model.all_ensembles[48]].pos = 700.000, 3725.000
gui[model.all_ensembles[48]].scale = 1.000
gui[model.all_ensembles[49]].pos = 700.000, 3800.000
gui[model.all_ensembles[49]].scale = 1.000
gui[model.all_ensembles[50]].pos = 700.000, 3875.000
gui[model.all_ensembles[50]].scale = 1.000
gui[model.all_ensembles[51]].pos = 700.000, 3950.000
gui[model.all_ensembles[51]].scale = 1.000
gui[model.all_ensembles[52]].pos = 700.000, 4025.000
gui[model.all_ensembles[52]].scale = 1.000
gui[model.all_ensembles[53]].pos = 700.000, 4100.000
gui[model.all_ensembles[53]].scale = 1.000
gui[model.all_ensembles[54]].pos = 700.000, 4175.000
gui[model.all_ensembles[54]].scale = 1.000
gui[model.all_ensembles[55]].pos = 700.000, 4250.000
gui[model.all_ensembles[55]].scale = 1.000
gui[model.all_ensembles[56]].pos = 700.000, 4325.000
gui[model.all_ensembles[56]].scale = 1.000
gui[model.all_ensembles[57]].pos = 700.000, 4400.000
gui[model.all_ensembles[57]].scale = 1.000
gui[model.all_ensembles[58]].pos = 700.000, 4475.000
gui[model.all_ensembles[58]].scale = 1.000
gui[model.all_ensembles[59]].pos = 700.000, 4550.000
gui[model.all_ensembles[59]].scale = 1.000
gui[model.all_ensembles[60]].pos = 700.000, 4625.000
gui[model.all_ensembles[60]].scale = 1.000
gui[model.all_ensembles[61]].pos = 700.000, 4700.000
gui[model.all_ensembles[61]].scale = 1.000
gui[model.all_ensembles[62]].pos = 700.000, 4775.000
gui[model.all_ensembles[62]].scale = 1.000
gui[model.all_ensembles[63]].pos = 700.000, 4850.000
gui[model.all_ensembles[63]].scale = 1.000
gui[model.all_ensembles[64]].pos = 700.000, 4925.000
gui[model.all_ensembles[64]].scale = 1.000
gui[model.all_ensembles[65]].pos = 700.000, 5000.000
gui[model.all_ensembles[65]].scale = 1.000
gui[model.all_ensembles[66]].pos = 700.000, 5075.000
gui[model.all_ensembles[66]].scale = 1.000
gui[model.all_ensembles[67]].pos = 700.000, 5150.000
gui[model.all_ensembles[67]].scale = 1.000
gui[model.all_ensembles[68]].pos = 700.000, 5225.000
gui[model.all_ensembles[68]].scale = 1.000
gui[model.all_ensembles[69]].pos = 700.000, 5300.000
gui[model.all_ensembles[69]].scale = 1.000
gui[model.all_ensembles[70]].pos = 700.000, 5375.000
gui[model.all_ensembles[70]].scale = 1.000
gui[model.all_ensembles[71]].pos = 700.000, 5450.000
gui[model.all_ensembles[71]].scale = 1.000
gui[model.all_ensembles[72]].pos = 700.000, 5525.000
gui[model.all_ensembles[72]].scale = 1.000
gui[model.all_ensembles[73]].pos = 700.000, 5600.000
gui[model.all_ensembles[73]].scale = 1.000
gui[model.all_ensembles[74]].pos = 700.000, 5675.000
gui[model.all_ensembles[74]].scale = 1.000
gui[model.all_ensembles[75]].pos = 700.000, 5750.000
gui[model.all_ensembles[75]].scale = 1.000
gui[model.all_ensembles[76]].pos = 700.000, 5825.000
gui[model.all_ensembles[76]].scale = 1.000
gui[circonv2.product.product.input].pos = 575.000, 4512.500
gui[circonv2.product.product.input].scale = 1.000
gui[circonv2.product.product.output].pos = 825.000, 4475.000
gui[circonv2.product.product.output].scale = 1.000
gui[circonv2.product.product.product].pos = 825.000, 4550.000
gui[circonv2.product.product.product].scale = 1.000
