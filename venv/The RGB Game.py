import numpy as np

class Game:
    def __init__(self):
        self.score = 0
        self.game_number = 0
        self.y = 10
        self.x = 15
        self.table = []
        self.clusters = []

    def InputData(self):
        for i in range(self.y):
            self.table.append([])
            self.table[i] = [str(a) for a in input()]
        for i in range(self.y):
            for j in range(self.x):
                self.table[i][j].strip()

    def ClearData(self):
        self.score = 0
        self.game_number = 0
        self.table = []
        self.clusters = []
    '''
    define all the clusters with dots in them to delete one by one
    '''
    def DefineClusters(self):
        self.clusters = []
        for i in range(self.y):
            for j in range(self.x):
                for k in range (1,2):
                    if i != 0:
                        if self.table[i][j] == self.table[i - 1][j] and self.table[i][j] != " ":
                            lowerDotClusterIndex = self.FindClusterOnDot(j, i-1)
                            currentDotClusterIndex = self.FindClusterOnDot(j, i)
                            if lowerDotClusterIndex == -1:
                                if currentDotClusterIndex == -1:
                                    self.clusters.append([])
                                    self.clusters[len(self.clusters) - 1].append(
                                        dict(map(lambda *args: args, ['x', 'y'], [j, i])))
                                    self.clusters[len(self.clusters) - 1].append(
                                        dict(map(lambda *args: args, ['x', 'y'], [j, i-1])))
                                else:
                                    self.clusters[currentDotClusterIndex].append(
                                        dict(map(lambda *args: args, ['x', 'y'], [j, i-1])))
                            else:
                                if currentDotClusterIndex == -1:
                                    self.clusters[lowerDotClusterIndex].append(
                                        dict(map(lambda *args: args, ['x', 'y'], [j, i])))
                                else:
                                    if lowerDotClusterIndex != currentDotClusterIndex:
                                        self.MergeClusters(lowerDotClusterIndex, currentDotClusterIndex)
                    if j != 0:
                        if self.table[i][j] == self.table[i][j-1] and self.table[i][j] != " ":
                            prevDotClusterIndex = self.FindClusterOnDot(j-1, i)
                            currentDotClusterIndex = self.FindClusterOnDot(j, i)
                            if prevDotClusterIndex == -1:
                                if currentDotClusterIndex == -1:
                                    self.clusters.append([])
                                    self.clusters[len(self.clusters) - 1].append(
                                        dict(map(lambda *args: args, ['x', 'y'], [j, i])))
                                    self.clusters[len(self.clusters) - 1].append(
                                        dict(map(lambda *args: args, ['x', 'y'], [j-1, i])))
                                else:
                                    self.clusters[currentDotClusterIndex].append(
                                        dict(map(lambda *args: args, ['x', 'y'], [j-1, i])))
                            else:
                                if currentDotClusterIndex == -1:
                                    self.clusters[prevDotClusterIndex].append(
                                        dict(map(lambda *args: args, ['x', 'y'], [j, i])))
                                else:
                                    if prevDotClusterIndex != currentDotClusterIndex:
                                        self.MergeClusters(prevDotClusterIndex, currentDotClusterIndex)
        for cluster in self.clusters:
            sorted(cluster, key=lambda dot: (dot['y'], dot['x']))

    '''
    delete cluster on index
    '''
    def DeleteCluster(self, clusterIndex):
        cluster = self.clusters[clusterIndex]
        for i in range(len(cluster)):
            self.table[cluster[i]['y']][cluster[i]['x']] = " "
        self.clusters.pop(clusterIndex)

    '''
    find biggest cluster
    '''
    def FindBiggestCluster(self):
        max = 0
        biggestClusterIndex = -1
        for cluster in self.clusters:
            if len(cluster) > max:
                max = len(cluster)
                biggestClusterIndex = self.clusters.index(cluster)
        return biggestClusterIndex

    '''
    return cluster's index by dot's coordinates
    '''
    def FindClusterOnDot(self, x, y):
        dotClusterIndex = -1
        for cluster in self.clusters:
            for dot in cluster:
                if x == dot["x"] and y == dot["y"]:
                    dotClusterIndex = self.clusters.index(cluster)
                    break
        return dotClusterIndex

    '''
    merge 2 clusters
    '''
    def MergeClusters(self, clusterIndex1, clusterIndex2):
        for dot in self.clusters[clusterIndex2]:
            if dot not in self.clusters[clusterIndex1]:
                self.clusters[clusterIndex1].append(dot)
        self.clusters.pop(clusterIndex2)
        return clusterIndex1

    '''
    move all dots down and left
    '''
    def MoveAllDown(self):
        tableTranspose = np.matrix(self.table).transpose().tolist()

        for i in range(self.x):
            tableTranspose[i] = tableTranspose[i][::-1]

        spaceCounter = 0
        for i in range(self.x):
            spaceCounter = tableTranspose[i].count(" ")
            tableTranspose[i] = "".join(str(e) for e in tableTranspose[i])
            tableTranspose[i] = tableTranspose[i].replace(" ", "")
            for space in range(spaceCounter):
                tableTranspose[i] += " "
            spaceCounter = 0

        for i in range(self.x):
            if not ("R" in tableTranspose[i] or "G" in tableTranspose[i] or "B" in tableTranspose[i]):
                temp = tableTranspose[i]
                tableTranspose.pop(i)
                tableTranspose.append(temp)
            tableTranspose[i] = tableTranspose[i][::-1]
            tableTranspose[i] = [x for x in tableTranspose[i]]

        self.table = np.matrix(tableTranspose).transpose().tolist()

    '''
    start the algorithm
    '''
    def Play(self):
        try:
            print("Game " + str(self.game_number) + ":")
            self.DefineClusters()
            move = 1
            biggestClusterIndex = self.FindBiggestCluster()
            while (biggestClusterIndex != -1):
                clusterToDelete = self.clusters[biggestClusterIndex]
                scoreToAdd = (len(clusterToDelete) - 2)**2
                color = self.table[clusterToDelete[0]['y']][clusterToDelete[0]['x']]
                print("Move " + str(move) + " at (" + str(9-clusterToDelete[0]['y']) + ", " + str(clusterToDelete[0]['x']) +
                      "): removed " + str(len(clusterToDelete)) + " balls of color " + color + ", got " + str(scoreToAdd) + " points.")
                self.score += scoreToAdd
                self.DeleteCluster(biggestClusterIndex)
                self.MoveAllDown()
                self.DefineClusters()
                biggestClusterIndex = self.FindBiggestCluster()
                move += 1
                # break
            ballsRemaining = 0
            for i in range(self.y):
                for j in range(self.x):
                    if "R" in self.table[i][j] or "G" in self.table[i][j] or "B" in self.table[i][j]:
                        ballsRemaining += 1
            if ballsRemaining == 0:
                self.score += 1000
            print("Final score: " + str(self.score) + ", with " + str(ballsRemaining) + " balls remaining.")
        except Exception as e:
            print(e)

    def StartGame(self):
        numberOfGames = int(input())
        for i in range(numberOfGames):
            self.game_number = i+1
            self.InputData()
            self.Play()
            self.ClearData()

Game().StartGame()
