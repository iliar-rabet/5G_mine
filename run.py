import sys
from TerrainProcessor import TerrainProcessor
from SolverSA import SolverSA

import pickle

# to deserialize the object
with open(sys.argv[1]+".dump", "rb") as input:
    TP = pickle.load(input) # protocol version is auto detected

    print(TP.periods,TP.max_x,TP.max_y)

    solver=SolverSA(TP,10)
    solver.deploy(0.4,0.5)