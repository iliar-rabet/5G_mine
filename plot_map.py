from mpl_toolkits import mplot3d


import sys
from TerrainProcessor import TerrainProcessor
from SolverSA import SolverSA
import random

import pickle

# # to deserialize the object
# with open("data.dump", "rb") as input:
#     obj = cPickle.load(input) # protocol version is auto detected

BlockName = 'maps/'+sys.argv[1]+'/'+sys.argv[1]+'.sol'
f = open ( BlockName , 'r')
Sol = []
Sol = [ line.split() for line in f]
# print(Sol)

SolName = 'maps/'+sys.argv[1]+'/'+sys.argv[1]+'.blocks'
f = open ( SolName , 'r')
blocks = []
blocks = [ line.split() for line in f]


TP = TerrainProcessor(blocks)
TP.process_sol(Sol)

# to serialize the object
with open(sys.argv[1]+".dump", "wb") as output:
    pickle.dump(TP, output, pickle.HIGHEST_PROTOCOL)

# solver=SolverSA(TP,10)
# solver.deploy(0.4,0.5)