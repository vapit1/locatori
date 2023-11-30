import numpy as np

class ClassGoals:
    def getClassName(self, tAnt, indMin, Wpt, koefHelPClassObj):
        coefSmal = 0.7e8 * np.exp(-0.9 * tAnt[indMin]) * koefHelPClassObj
        coefMedium = 1.55e8 * np.exp(-0.9 * tAnt[indMin]) * koefHelPClassObj
        coefBig = 3.2e8 * np.exp(-0.9 * tAnt[indMin]) * koefHelPClassObj

        coefSig = np.max(Wpt)

        if coefSig < coefSmal:
            return 'Буй'
        elif coefSig > coefSmal and coefSig < coefBig:
            return 'НПА'
        elif coefSig > coefBig:
            return 'АПЛ'
