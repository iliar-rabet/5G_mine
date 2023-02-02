from OF import OF 
import random
import math

class SolverSA():
    def __init__(self, TP, NCandidateBSs):
        self.of=OF()
        self.TP = TP
        # print(TP.terrain)
        self.PermBS=0
        self.TempBS=0
        self.CandidateBSs=self.generateCandidates(10,0)
        self.CandidateCoWs=self.generateCandidateCoWs(10,0)
        self.numCandidates = 15
        self.numTempCandidates = 20


    def final(self,point,p):
        if self.TP.Zs[p][point["X"]][point["Y"]] == self.TP.Zs[self.TP.periods-1][point["X"]][point["Y"]]:
            return True

    def generateCandidateCoWs(self, N,p):
        Candidates = []
        x=0
        while x<N:
        
            newBS = {
                "range": 30,
                "elevation": 0
            }
            newBS["X"]=random.randint(0,self.TP.max_x-1)
            newBS["Y"]=random.randint(0,self.TP.max_y-1)
            if self.TP.Zs[0][newBS["X"]][newBS["Y"]] != 0:
                Candidates.append(newBS)
                x += 1 
        return Candidates

    def generateCandidates(self, N ,p):
        Candidates = []
        x=0
        while x<N:
        
            newBS = {
                "range": 50,
                "elevation": 0
            }
            newBS["X"]=random.randint(0,self.TP.max_x-1)
            newBS["Y"]=random.randint(0,self.TP.max_y-1)
            if self.final(newBS,p) and self.TP.Zs[0][newBS["X"]][newBS["Y"]] != 0:
                print(self.TP.Zs[0][newBS["X"]][newBS["Y"]])
                Candidates.append(newBS)
                x += 1 
        
        print(Candidates)
        
        return Candidates

    def InitDeployPerm(self):
        # print(self.PermBS)
        # print(len(self.CandidateBSs))
        dep=random.sample(self.CandidateBSs, self.PermBS)
        return dep

    def InitDeployTemp(self):
        # print(self.PermBS)
        # print(len(self.CandidateBSs))
        if self.TempBS>len(self.CandidateCoWs):
            print("too many TempBS")
        dep=random.sample(self.CandidateCoWs, self.TempBS)
        return dep

    def changeBS(self, currDep,currCoWs):
        r = random.randint(0,100)
        if self.TempBS==0 or r < 50:
            DepInd = random.randint(0,self.PermBS-1)
            newInd = random.randint(0,len(self.CandidateBSs)-1)
            newDep = currDep.copy()
            # print(DepInd, len(currDep),self.PermBS, newInd,len(self.CandidateBSs))
            newDep[DepInd] = self.CandidateBSs[newInd]
            return currCoWs, newDep
        else:
            DepInd = random.randint(0,self.TempBS-1)
            newInd = random.randint(0,len(self.CandidateCoWs)-1)
            newCoWs= currCoWs.copy()
            newCoWs[DepInd] = self.CandidateCoWs[newInd]
            return newCoWs, currDep
        
        
    def deploy(self,thPerm, thTemp):
        ObjPer = 0
        for p in range(self.TP.periods):
            
            # self.CandidateBSs=self.generateCandidates(self.numCandidates,p)
            # while(ObjPer < thPerm):
            while(self.PermBS < 5):
                self.PermBS+=1
                # self.filter(self.CandidateBSs)
                dep,CoWs=self.solve(100)
                ObjPer=self.of.Objective(self.TP, dep, log=1)
                print("period, Objective, permBS")
                print(p , ObjPer, self.PermBS)
        
        ObjPer = 0
        for p in range(self.TP.periods):            
            self.CandidateCoWs=self.generateCandidateCoWs(self.numTempCandidates,p)
            # while(ObjPer < thTemp):
            while(self.TempBS < 5):
                self.TempBS+=1
                # self.filter(self.CandidateBSs)
                dep,CoWs=self.solve(200)
                ObjPer=self.of.Objective(self.TP, dep,log=1)
                print("period, Objective, permBS, TempBS")
                print(p , ObjPer, self.PermBS, self.TempBS)

        self.TP.plot_terrain(self.TP.Zs[self.TP.periods-1])
        # self.TP.plot_2d(self.TP.Zs[self.TP.periods-1],dep)
        
        
                

    def solve(self, iterations, init_temp = 100):
        currDep = self.InitDeployPerm()
        if self.TempBS > 0: currCoWs = self.InitDeployTemp()
        else: currCoWs=[]
        currOF = self.of.Objective(self.TP,currDep,currCoWs) 
        for iter in range(iterations):
            newCoWs, newDep = self.changeBS(currDep,currCoWs)
            newOF=self.of.Objective(self.TP,newDep,newCoWs)

            diff = newOF - currOF
            
            t = init_temp / float(iter + 1)
            # print("temp:"+str(t) + " init_temp: "+ str(init_temp) )
            
            metropolis = 0
            if diff < -100:
                diff = -100
            if diff < 0:
                metropolis = math.exp(diff / t)
            
            if diff > 0 or random.random() < metropolis:
                # if iter % 2 == 0:
                # print("eval: ", currOF, currDep)
                # print("accept new solution")
                currOF = newOF
                currDep = newDep
                currCoWs = newCoWs
            # else:
            #     print("reject new solution")
        
        return currDep,currCoWs