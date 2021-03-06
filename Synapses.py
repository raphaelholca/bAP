'''
Created on Dec 5, 2012

@author: raphaelholca
'''

from numpy import *

class Synapses(object):
    
    def __init__(self, sim, preName, postName, pre, post, size, g, weightRand, g_min, g_max, rise, decay, E, extent=None):
        ''' 
        Object Constructor 
        '''
        
        #synapse parameters
        self.preName = preName #name of the pre-synaptic population
        self.postName = postName #name of the post-synpatic population
        self.pre = pre #pointer to the pre-synaptic population
        self.post = post #pointer to the post-synaptic population
        self.size = size #size of the synapse matrix
        self.g_min = g_min #minimal value an AMPA synaptic weight can take
        self.g_max = g_max #maximal value an AMPA synaptic weight can take
        self.g_max_matrix = ones(size)*g_max #matrix of maximal connection weights for the lateral connections
        self.rise = ones(size)*rise #rise time constant of the open probability
        self.decay = decay #decay time constant of the open probability
        self.E = E #reversal potential of the synaptic current
        self.extent = extent #parameter setting the spatial extent of lateral connections
        if weightRand==0:weightRand=1e-99
        
        #synapse variables
        self.I_NMDA = zeros(size) #Ca2+ current through NMDAr
        self.I_VGCC = zeros(size) #Ca2+ current through voltage-gated calcium channels
        self.I = zeros(size) #current through AMPAr and GABAr
        self.Vm = ones(size)*sim.Vreset #local membrane potential at the synapse
        self.Mg = zeros(size) #extent of the Mg blockade of the NMDAr
        self.g = clip(random.normal(g,weightRand,size),0,g_max) #initialize the synaptic weights 
        self.calcium = ones(size)*sim.Crest #zeros(size) #internal "calcium" concentration, used to compute LTD
        
        self.V_BPAP = zeros(1) #depolarization due to the back-propagating action-potential
        self.VmPSP = ones(size)*sim.Vreset #membrane potential at the synapse only due to PSP (does not include the bAP)
        self.lastSynsSpike = ones(size)*-1e99 #time of last pre-synaptic spike
        self.risingBool = array([[False]*size[1]]*size[0]) #boolean indicator of whether the open probability is in the rising or decaying phase 
        
        #calcium detectors
        self.P=zeros(size)
        self.V=zeros(size)
        self.B=zeros(size)
        self.D=zeros(size)
