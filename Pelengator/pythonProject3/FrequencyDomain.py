import numpy as np
import math

class FrequencyDomain:
    def getArrForFft(self, SS, M, iK, iN):
        SS_f = np.zeros((M, iK - iN + 1))
        for k in range(0, M):
            counter_j = 0
            for l in range(iN, iK):
                SS_f[k][counter_j] = SS[k][l]
                counter_j = counter_j + 1
        return SS_f

    def getPhasingFactor(self, j, M, n, freq, b, d, c):
        T0 = d / c * math.sin(b[j])
        Tcomp = np.arange(M, 0, -1) * T0
        coef = np.zeros((M, n), dtype=complex)
        for l in range(0, M):
            coef[l] = np.exp(1j * 2 * math.pi * Tcomp[l] * freq)
        return coef

    def getResponse(self, kn, kv, AA):
        Z = np.array([])
        for k in range(kn, kv):
            Z = np.append(Z, np.absolute(AA[k]) ** 2)
        return Z