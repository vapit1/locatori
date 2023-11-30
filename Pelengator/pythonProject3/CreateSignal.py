import numpy as np
import math

class CreateSiganl:
    # конструктор
    def __init__(self, coefObj):
        self.coefObj = coefObj

    def getSignal(self, M, nwin, t, Tm1, f):
        s = np.zeros((M, nwin))
        for i in range(0, M):
            s[i] = np.sin(2 * math.pi * f * (t - Tm1[i])) * self.coefObj
        return s

    def getIntervalLaw(self, numStart, numEnd, tAnt):
        Tlow = np.array([])
        for i in range(numStart, numEnd + 1):
            Tlow = np.append(Tlow, tAnt[i])
        return Tlow

    def decayLaw(self, M, nwin, Tlow):
        lowSig = np.zeros((M, nwin))
        for i in range(0, M):
            lowSig[i] = np.exp(-0.9 * Tlow)
        return lowSig

    def getSumNoiseSignal(self,  M, numStart, numEnd, sNoise, sL):
        for i in range(0, M):
            k = 0
            for j in range(numStart, numEnd + 1):
                sNoise[i][j] = sL[i][k] + sNoise[i][j]
                k = k + 1
        return sNoise