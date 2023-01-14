import numpy as np

class Square:
    def __init__(self):
        self.linesCoords = []
        self.linesCoeffs = []
        self.Y_for_x0_Edges = [0]
        self.X_for_Y0_Edges = [0]
        self.Y_for_x100_Edges = [0]
        self.X_for_y100_Edges = [0]

    def InputData(self):
        numberOfLines = int(input())
        for i in range(numberOfLines):
            x1,y1,x2,y2 = map(int, input().split())
            self.linesCoords.append(dict(map(lambda *args: args, ['x1','y1','x2','y2'], [x1,y1,x2,y2])))
        
            if y1 == 0:
                self.X_for_Y0_Edges.append(x1)
            elif y1 == 100:
                self.X_for_y100_Edges.append(x1)
        
            if x1 == 0:
                self.Y_for_x0_Edges.append(y1)
            elif x1 == 100:
                self.Y_for_x100_Edges.append(y1)
        
            if y2 == 0:
                self.X_for_Y0_Edges.append(x2)
            elif y2 == 100:
                self.X_for_y100_Edges.append(x2)
        
            if x2 == 0:
                self.Y_for_x0_Edges.append(y2)
            elif x2 == 100:
                self.Y_for_x100_Edges.append(y2)
        
            k = (y1 - y2) / (x1 - x2)
            b = y2 - k * x2
            self.linesCoeffs.append(dict(map(lambda *args: args, ['k','b'], [k,b])))

        self.Y_for_x0_Edges.append(100)
        self.Y_for_x0_Edges.sort()
        self.X_for_Y0_Edges.append(100)
        self.X_for_Y0_Edges.sort()
        self.Y_for_x100_Edges.append(100)
        self.Y_for_x100_Edges.sort()
        self.X_for_y100_Edges.append(100)
        self.X_for_y100_Edges.sort()

        self.x0,self.y0 = map(float, input().split())
    '''
    the algorithm that counts all intersctions with all the lines and 
    lines between parts of the edges of a square and a point of treasure
    '''
    def Solve(self):
        min = 1000
        for i in range(1,len(self.Y_for_x0_Edges)):
            y_i = (self.Y_for_x0_Edges[i] + self.Y_for_x0_Edges[i-1])/2
            x_i = 0
            k = (self.y0 - y_i) / (self.x0 - x_i)
            b = self.y0 - k * self.x0
            baseLineCoeffs = dict(map(lambda *args: args, ['k','b'], [k,b]))
            linesCrossed = 0
            # for lines = self.linesCoeffs[0]:
            for lines in self.linesCoeffs:
                M = np.matrix([[baseLineCoeffs['k'], -1], [lines['k'], -1]])
                C = np.matrix([baseLineCoeffs['b'], lines['b']])
                cross_dot = -M.I.dot(C.T)
                if cross_dot[0] > 0 and cross_dot[0] < self.x0:
                    if cross_dot[1] > 0 and cross_dot[1] < 100:
                        if (cross_dot[1] < self.y0 and y_i < self.y0) or (cross_dot[1] > self.y0 and y_i > self.y0):
                            linesCrossed += 1
            if linesCrossed < min:
                min = linesCrossed
                y_min = y_i

        for i in range(1,len(self.Y_for_x100_Edges)):
            y_i = (self.Y_for_x100_Edges[i] + self.Y_for_x100_Edges[i-1])/2
            x_i = 100
            k = (self.y0 - y_i) / (self.x0 - x_i)
            b = self.y0 - k * self.x0
            baseLineCoeffs = dict(map(lambda *args: args, ['k','b'], [k,b]))
            linesCrossed = 0
            # for lines = self.linesCoeffs[0]:
            for lines in self.linesCoeffs:
                M = np.matrix([[baseLineCoeffs['k'], -1], [lines['k'], -1]])
                C = np.matrix([baseLineCoeffs['b'], lines['b']])
                cross_dot = -M.I.dot(C.T)
                if cross_dot[0] > self.x0 and cross_dot[0] < 100:
                    if cross_dot[1] > 0 and cross_dot[1] < 100:
                        if (cross_dot[1] < self.y0 and y_i < self.y0) or (cross_dot[1] > self.y0 and y_i > self.y0):
                            linesCrossed += 1
            if linesCrossed < min:
                min = linesCrossed
                y_min = y_i

        for i in range(1,len(self.X_for_Y0_Edges)):
            y_i = 0
            x_i = (self.X_for_Y0_Edges[i] + self.X_for_Y0_Edges[i-1])/2
            k = (self.y0 - y_i) / (self.x0 - x_i)
            b = self.y0 - k * self.x0
            baseLineCoeffs = dict(map(lambda *args: args, ['k','b'], [k,b]))
            linesCrossed = 0
            # for lines = self.linesCoeffs[0]:
            for lines in self.linesCoeffs:
                M = np.matrix([[baseLineCoeffs['k'], -1], [lines['k'], -1]])
                C = np.matrix([baseLineCoeffs['b'], lines['b']])
                cross_dot = -M.I.dot(C.T)
                if cross_dot[1] > 0 and cross_dot[1] < self.y0:
                    if cross_dot[0] > 0 and cross_dot[0] < 100:
                        if (cross_dot[0] < self.x0 and x_i < self.x0) or (cross_dot[0] > self.x0 and x_i > self.x0):
                            linesCrossed += 1
            if linesCrossed < min:
                min = linesCrossed
                x_min = x_i

        for i in range(1,len(self.X_for_y100_Edges)):
            y_i = 100
            x_i = (self.X_for_y100_Edges[i] + self.X_for_y100_Edges[i-1])/2
            k = (self.y0 - y_i) / (self.x0 - x_i)
            b = self.y0 - k * self.x0
            baseLineCoeffs = dict(map(lambda *args: args, ['k','b'], [k,b]))
            linesCrossed = 0
            # for lines = self.linesCoeffs[0]:
            for lines in self.linesCoeffs:
                M = np.matrix([[baseLineCoeffs['k'], -1], [lines['k'], -1]])
                C = np.matrix([baseLineCoeffs['b'], lines['b']])
                cross_dot = -M.I.dot(C.T)
                if cross_dot[1] > self.y0 and cross_dot[1] < 100:
                    if cross_dot[0] > 0 and cross_dot[0] < 100:
                        if (cross_dot[0] < self.x0 and x_i < self.x0) or (cross_dot[0] > self.x0 and x_i > self.x0):
                            linesCrossed += 1
            if linesCrossed < min:
                min = linesCrossed
                x_min = x_i
        
        min+=1
        return min

    def Start(self):
        self.InputData()
        self.Solve()
        print("Number of doors = " + str(self.Solve()))

Square().Start()

