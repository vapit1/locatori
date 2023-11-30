class DataWorkAlgoritm:
    def __init__(self, distance, peleng, classGoals):
        self.distance = distance
        self.peleng = peleng
        self.classGoals = classGoals

    def getDistance(self):
        return str(self.distance)

    def getPeleng(self):
        return str(self.peleng)

    def getName(self):
        return self.classGoals
