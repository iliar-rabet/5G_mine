import matplotlib.pyplot as plt
import numpy as np
import copy

class TerrainProcessor():
    def init_terrain(self):
        self.terrain = [[[] for j in range(self.max_y)] for i in range(self.max_x)]
    

    def __init__(self,blocks):
        self.max_x=0
        self.max_y=0
        self.periods = 0
        self.blocks = blocks
        self.Zs=[]
        for b in blocks:
            if int(b[1])>self.max_x:
                self.max_x = int(b[1])
            if int(b[2])>self.max_y:
                self.max_y = int(b[2])
        self.max_x = self.max_x + 1
        self.max_y = self.max_y + 1
        print("max_x "+str(self.max_x))
        print("max_y "+str(self.max_y))
        self.init_terrain()
        self.cal_terrain(blocks)
        # self.Z = [ [1]*self.max_x for i in range(self.max_y)]

    def cal_terrain(self,blocks):
        for b in blocks:
            x_ind=int(b[1])
            y_ind=int(b[2])
            self.terrain[x_ind][y_ind].append(int(b[3])) 
            # print(terrain)
            # print("setting " + str(x_ind) + " and " + str(y_ind) + " is: " + str(terrain[x_ind][y_ind]) + "\n")


    def cal_z(self, terrain):
        newZ = [[0 for j in range(self.max_y)] for i in range(self.max_x)]
        for i in range(self.max_x):
            for j in range(self.max_y):
                # print("terrain at " + str(i) + " and " + str(j) + " is: " + str(terrain[i][j]) + "\n")
                if terrain[i][j]==[]:
                    newZ[i][j]=0
                else:
                    newZ[i][j] = max(terrain[i][j])
        return newZ
    
    def process_sol(self, sol):
        for s in sol:
            if (int(s[2])+1) >self.periods:
                self.periods = int(s[2])+1

        print("periods: " + str(self.periods))
        moved_blocks=[]
        
        for period in range(self.periods):      
            for b in sol:
                if(int(b[2])==period):
                    moved_blocks.append(b[0])
            
            new_terrain = None
            if new_terrain is None:
                new_terrain = copy.deepcopy(self.terrain)
            else:
                new_terrain = copy.deepcopy(new_terrain)

            for mb in moved_blocks:
                for b in self.blocks:
                    if b[0] == mb:
                        x=int(b[1])
                        y=int(b[2])
                        new_terrain[x][y].remove(int(b[3]))

            # print(new_terrain)
            tmp_elevation = self.cal_z(new_terrain)
            self.Zs.append(tmp_elevation)
            # self.plot_terrain(tmp_elevation)
            # print(tmp_elevation)
        

    def plot_terrain(self,Z):
        y = range(self.max_x)
        x = range(self.max_y)
        X, Y = np.meshgrid(x, y)

        fig = plt.figure()
        ax = plt.axes(projection='3d')
        ax.contour3D(X, Y, Z, 50,  cmap='viridis', edgecolor=None)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        plt.show()

    def plot_2d(self,Z,Dep):
        y = range(self.max_x)
        x = range(self.max_y)
        X, Y = np.meshgrid(x, y)

        fig = plt.figure()
        ax = fig.add_subplot(111)

        cp = ax.contour(X, Y, Z)
        ax.clabel(cp, fontsize=10)
        # plt.xticks([0,0.5,1])
        # plt.yticks([0,0.5,1])
        ax.set_xlabel('X-axis')
        _ = ax.set_ylabel('Y-axis')
        plt.show()
