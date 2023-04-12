import math
from typing import List


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
    if dx >= dy and dx >= dz:
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
    elif dy >= dx and dy >= dz:
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
        while z1 != z2:
            z1 += zs
            if p1 >= 0:
                y1 += ys
                p1 -= 2 * dz
            if p2 >= 0:
                x1 += xs
                p2 -= 2 * dz
            p1 += 2 * dy
            p2 += 2 * dx
            ListOfPoints.append((x1, y1, z1))
    return ListOfPoints



class OF():
    def __init__(self):
        self.gamma = 0.5
        print("OF")

    def los_check(self, BS, TGx, TGy, Z):
        # print(len(Z))
        # print(TGx,TGy,Z[TGx][TGy])
        # print(BSx,BSy,len(Z[BSx]))
        # print("--")
        BSx = BS.X
        BSy = BS.Y
        line = Bresenham3D(BSx, BSy, Z[BSx][BSy], TGx, TGy, Z[TGx][TGy])

        for point in line:
            if point[2] < Z[point[0]][point[1]]:
                # print("no line of sight")
                return False, point[0], point[1]
        return True, 0, 0

    def Coverage_Prob(self, Z, i, j, BS):
        Mult = 1
        for currBS in BS:
            d = dist(currBS, Z, i, j)
            # print("d:"+str(d))
            if d < currBS.range:
                if self.los_check(currBS, i, j, Z):
                    p = 1
                else:
                    p = self.gamma * d / currBS.range
            else:
                p = 0
            Mult = Mult * (1 - p)
        prob = (1 - Mult)
        return prob

    def distance(self, Px, Py, i , j):
        tmp = pow((Px - i), 2) + pow((Py - j), 2)
        return math.sqrt(tmp)*5
    def FR(self,v):
        if v <= -1:
            return 1
        if -1 < v <= 0:
            return 0.5 - 0.62 *v
        if 0 < v <= 1:
            return 0.5 * math.exp(-0.95*v)
        if 1 < v <= 2.4:
            return 0.4 - math.sqrt(0.1184 - pow((0.38 - 0.1 * v), 2))
        if v > 2.4:
            return 0.225/v
        print(v)
    def P_from_BS(self, Z, i, j, currBS):
        d = self.distance(currBS.X, currBS.Y, i, j)
        if d == 0:
            return 0
        if d > currBS.range:
            return -105
        wave = 0.125
        h1 = Z[i][j]
        h2 = Z[currBS.X][currBS.Y]

        Los, OBSx, OBSy = self.los_check(currBS, i, j, Z)
        if Los:
            LD = 0
        else:
            d1 = self.distance(OBSx, OBSy, i, j)
            d2 = self.distance(currBS.X, currBS.Y, i, j)
            hobs = Z[OBSx][OBSy]
            h = hobs - (d1 * (h2 - h1))/(d1 + d2) - h1
            v = h * math.sqrt(2*(d1+d2)/wave * d1 * d2)
            Frenzel = self.FR(v)
            if Frenzel is None:
                print(v)
            LD = 20 * math.log10(Frenzel)

        FSPL = 20 * math.log10(d) + 10 * math.log10(currBS.f) - 27.5
        PL = FSPL + LD + currBS.k * math.log10(currBS.elevation)
        # print("i,j:"+str(i) +"," + str(j) + " BS:" + str(currBS.X) +"," + str(currBS.Y) )
        # print("d:"+str(d) + " FSPL:"+str(FSPL)+" PL:"+str(PL)+ " LD" + str(LD))
        return currBS.TXP - PL

    def interference(self, arr):
        sublist = [x for x in arr if x < max(arr)]
        if not sublist:
            return -95
        return max(sublist)
    def SINR(self, Z, i, j, BS):
        noise = -95
        lsRSS = []
        for currBS in BS:
            lsRSS.append(self.P_from_BS(Z, i, j, currBS))

        bestRSS = max(lsRSS)

        interference = self.interference(lsRSS)
        interference = max(interference, noise)
        SINR = max(lsRSS) - interference
        # for i in lsRSS:
        #     lsSINR.append(i / (noise + S - i) )
        if SINR < -10 :
            print("RSS")
            print(lsRSS)
            print("SINR")
            print(SINR)

        return SINR

    def Objective(self, TP, BS, log=0):
        Obj = 0.0
        # print(BS)
        # print("TP.periods"+str(TP.periods))

        for period, z in enumerate(TP.Zs):
            period_sum = 0.0

            SINR_MAP = [[self.SINR(z, i, j, BS) for j in range(TP.max_y)] for i in range(TP.max_x)]
            period_sum = sum(sum(SINR_MAP, []))
            Obj += period_sum

            if log == 1:
                # print(period, period_sum / (TP.max_x * TP.max_y))
                print(str(period_sum / (TP.max_x * TP.max_y)) + ", ")

        return Obj / (TP.max_x * TP.max_y * TP.periods)