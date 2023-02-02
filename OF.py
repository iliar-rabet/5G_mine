import math


def Bresenham3D(x1, y1, z1, x2, y2, z2):
    ListOfPoints = []
    ListOfPoints.append((x1, y1, z1))
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    dz = abs(z2 - z1)
    if (x2 > x1):
        xs = 1
    else:
        xs = -1
    if (y2 > y1):
        ys = 1
    else:
        ys = -1
    if (z2 > z1):
        zs = 1
    else:
        zs = -1
 
    # Driving axis is X-axis"
    if (dx >= dy and dx >= dz):       
        p1 = 2 * dy - dx
        p2 = 2 * dz - dx
        while (x1 != x2):
            x1 += xs
            if (p1 >= 0):
                y1 += ys
                p1 -= 2 * dx
            if (p2 >= 0):
                z1 += zs
                p2 -= 2 * dx
            p1 += 2 * dy
            p2 += 2 * dz
            ListOfPoints.append((x1, y1, z1))
 
    # Driving axis is Y-axis"
    elif (dy >= dx and dy >= dz):      
        p1 = 2 * dx - dy
        p2 = 2 * dz - dy
        while (y1 != y2):
            y1 += ys
            if (p1 >= 0):
                x1 += xs
                p1 -= 2 * dy
            if (p2 >= 0):
                z1 += zs
                p2 -= 2 * dy
            p1 += 2 * dx
            p2 += 2 * dz
            ListOfPoints.append((x1, y1, z1))
 
    # Driving axis is Z-axis"
    else:
        p1 = 2 * dy - dz
        p2 = 2 * dx - dz
        while (z1 != z2):
            z1 += zs
            if (p1 >= 0):
                y1 += ys
                p1 -= 2 * dz
            if (p2 >= 0):
                x1 += xs
                p2 -= 2 * dz
            p1 += 2 * dy
            p2 += 2 * dx
            ListOfPoints.append((x1, y1, z1))
    return ListOfPoints
 

def dist( currBS,Z,i,j):
    tmp=pow((currBS["X"] - i),2) +pow((currBS["Y"] - j),2) + pow((Z[currBS["X"]][currBS["Y"]]+ currBS["elevation"] - Z[i][j]),2)
    return math.sqrt(tmp)

class OF():
    def __init__(self):
        self.gamma = 0.5
        print("OF")

    def los_check(self, BS, TGx, TGy,Z):
        # print(len(Z))
        # print(TGx,TGy,Z[TGx][TGy])
        # print(BSx,BSy,len(Z[BSx]))
        # print("--")
        BSx=BS["X"]
        BSy=BS["Y"]
        line= Bresenham3D(BSx,BSy,Z[BSx][BSy], TGx,TGy,Z[TGx][TGy])
        
        for point in line:
            if point[2] < Z[point[0]][point[1]]:
                # print("no line of sight")
                return False
        return True

    def Coverage_Prob(self, Z,i,j,BS):
        Mult = 1
        for currBS in BS:
            d=dist(currBS,Z,i,j)
            # print("d:"+str(d))
            if d < currBS["range"]:
                if self.los_check(currBS,i,j,Z):
                    p = 1
                else:
                    p = self.gamma * d / currBS["range"]
            else:
                p = 0
            Mult = Mult * (1-p)
        prob = (1 - Mult)
        return prob


    def Objective(self, TP,BS, log=0):
        Obj=0.0
        # print(BS)
        # print("TP.periods"+str(TP.periods))
        for period, z in enumerate(TP.Zs):
            period_sum=0.0
            for i in range(TP.max_x):
                for j in range(TP.max_y):
                    point=self.Coverage_Prob(z,i,j,BS)
                    period_sum = period_sum + point
                    Obj = Obj + point
            if log==1:
                print(period, period_sum/(TP.max_x * TP.max_y))
        Obj = Obj / (TP.max_x * TP.max_y * TP.periods)
        return Obj
