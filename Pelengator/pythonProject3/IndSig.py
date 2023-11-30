import numpy as np
from scipy.signal import butter, lfilter, hilbert

class IndSig():
    def bandPassFilter(self, sMod, fd):  # фильтрация сигнала полосовым фильтром
        order = 6  # порядок
        nyq = 0.5 * fd  # полоса работы фильтра
        low = 1900 / nyq  # нижняя частота среза
        high = 2100 / nyq  # верхняя частота среза
        b, a = butter(order, [low, high], btype='band')  # коеф-нт фильтра
        return lfilter(b, a, sMod)  # фильтрация

    def pulseSignal(self, sFiltr, nAnt):  # формирование импульсного сигнала
        amplitudeS = np.abs(hilbert(sFiltr))  # огибающая сигнала

        imp = np.array([])
        for i in range(0, nAnt):
            if amplitudeS[i] > 0.2:
                imp = np.append(imp, 1)
            else:
                imp = np.append(imp, 0)

        return imp

    def getIndImp(self, up, nAnt):
        minUp, maxUp, k = 0, 0, 0
        arrInd = []
        for i in range(0, nAnt):
            if up[i] == 1:
                if maxUp == 0:
                    minUp = i

                if minUp != 0:
                    maxUp = i
            else:
                if (minUp != 0) and (maxUp != 0):
                    # arrInd [мин. индекс, макс. индекс, кол-во отсчетов импульса]
                    arrInd.append([minUp, maxUp, maxUp - minUp])
                    k = k + 1
                    minUp = 0
                    maxUp = 0

        sizeArr = np.array(arrInd).shape[0]  # кол-во строк массива

        if sizeArr == 1:
            return arrInd[0:2]
        else:
            longArrInd = np.array(arrInd)[:, 2]  # массив с длиннами импульсов
            return arrInd[np.argmax(longArrInd)][0:2]  # индексы самого длинного испульса
