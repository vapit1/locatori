from posixpath import defpath
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, hilbert

from CreateSignal import *
from ShowSignal import *
from IndSig import *
from FrequencyDomain import *
from ClassGoals import *
from DataWorkAlgoritm import *

def collBack(alfa, Long, coefObj, duration):
    c = 1500  # скорость звука
    d = 0.2  # расстояние между приемными элементами
    M = 30  # кол-во приемных элементов

    fd = 10000  # частота дискретизации
    dt = 1 / fd  # время 1 отсчета

    tMod = duration # время можелирования сигнала

    initialTime = 0.2
    koefHelPClassObj = tMod / initialTime

    t = np.arange(0, tMod, dt)  # массив времени работы активной ГАС
    nwin = t.size # кол-во отсчетов сигнала


    f = 2000  # частота сигнала
    fn = 1900  # нижняя частота пропускания
    fv = 2100  # верхняя частота пропускания

    n = 100  # кол-во точек БПФ
    df = fd / n  # шаг дискретизации в частотной области

    # формироваие полосы анализа сигнала
    freq = np.fft.fftfreq(n, d=dt)

    # индекс обработки
    kn = int(np.round(fn / df + 1, 0))  # для нижней частоты
    kv = int(np.round(fv / df + 1, 0))  # для верхней частоты

    T01 = np.sin(np.deg2rad(alfa)) * d / c  # задержка
    Tm1 = np.arange(M, 0, -1) * T01  # массив задержек


    tObr = 2  # время обработки сигнала активной ГАС
    tAnt = np.arange(0, tObr, dt)  # массив времени работы активной ГАС
    nAnt = tAnt.size  # кол-во точек массива времени

    numStart = int(round(((2 * Long / c) / dt), 0))  # начальный отсчет сигнала
    numEnd = int(numStart + nwin - 1)  # конечный отсчет сигнала

    createSiganl = CreateSiganl(coefObj)
    s = createSiganl.getSignal(M, nwin, t, Tm1, f) # тональный сигнал
    lowSig = createSiganl.decayLaw(M, nwin, createSiganl.getIntervalLaw(numStart, numEnd, tAnt)) # затухающие колебания
    sL = np.multiply(s, lowSig) # сигнал с затуханием амплитуды
    noise = 5 * np.random.normal(0, 0.1, size=(M, nAnt)) # Нормально распределенный шум
    Snoise = createSiganl.getSumNoiseSignal(M, numStart, numEnd, noise, sL) # сигнал на приемных элементах антенны

    sMod = Snoise[0]  # данные для нахождения сигнала на фоне шума

    showSignal = ShowSignal()
    showSignal.viewSignal(tAnt, sMod)

    indSig = IndSig()
    sFiltr = indSig.bandPassFilter(sMod, fd)  # полосовой фильтр
    imp = indSig.pulseSignal(sFiltr, nAnt)  # импульсный сигнал (аналог порогового устройства)
    indImp = indSig.getIndImp(imp, nAnt)  # индексы обнаруженного импульсного сигнала
    indImpReal = [np.mean(indImp) - nwin / 2, np.mean(indImp) + nwin / 2] # индексы сигнала для обработки
    indMin, indMax = int(indImpReal[0]), int(indImpReal[1])
    SS = Snoise[:, indMin : indMax] # сигнал для дальнейшей обработки

    showSignal.viewFilter(tAnt, sFiltr)

    N = int(round(len(t)/n, 0)) # число тактов обработки сигнала
    b = np.arange(-90, 90, 1) * math.pi / 180 # угол фазирования
    Wp = np.zeros((N, len(b)))

    freqDomain = FrequencyDomain()
    for i in range(1, N):
        iN = (i - 1) * n + 1  # начальное значение временного интервала
        iK = i * n  # конечное значение временного интервала
        SS_f = freqDomain.getArrForFft(SS, M, iK, iN)
        Vp = np.array([])  # отклик в такте обработки
        sf = np.fft.fft(SS_f, n, 1)
        for j in range(0, len(b)):
            coef = freqDomain.getPhasingFactor(j, M, n, freq, b, d, c)  # массив фазирующих коеф-нтов
            sfComp = np.multiply(sf, coef)  # компенсация временных задержек
            PK = np.sum(sfComp, axis=0)  # формирование ПК в направлении b
            Z = freqDomain.getResponse(kn, kv, PK)  # отклик в полосе обработки
            Vp = np.append(Vp, np.sum(Z, axis=0))
        Wp[i] = Vp

    Wpt = np.sum(Wp, axis=0)
    b = np.arange(-90, 90, 1)  # угол фазирования

    distance = int(np.round(tAnt[indMin]* c / 2, 0)) # дистанция
    peleng = int(b[np.argmax(Wpt)]) # пеленг

    showSignal.viewSetResponse(Wp, tAnt, indMax, indMin)
    showSignal.viewGridCoordinates(distance, peleng)

    classGoals = ClassGoals().getClassName(tAnt, indMin, Wpt, koefHelPClassObj)

    return DataWorkAlgoritm(distance, peleng, classGoals)

'''alfa = -60  # угол падения
Long = 1000  # расстояние
coefObj = 4 # коеф класс

dataObj = collBack(alfa, Long, coefObj)
peleng = dataObj.getDistance()
distance = dataObj.getPeleng()
nameObj = dataObj.getName()

print('Дистанция от антенны до цели ' + distance)
print('Пеленг на цель ' + peleng)
print(nameObj)'''

