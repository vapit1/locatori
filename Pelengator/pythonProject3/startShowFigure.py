import numpy as np
import matplotlib.pyplot as plt

def viewSignal():
    fig = plt.figure()
    plt.title('Сигнал на ПЭ')
    plt.xlabel('Время, с')
    plt.ylabel('Амплитуда сигнала')
    fig.savefig('signal.png', dpi=65)
def viewFilter():
    fig = plt.figure()
    plt.title('Фильтрация сигнала')
    plt.xlabel('Время, с')
    plt.ylabel('Амплитуда сигнала')
    fig.savefig('filter.png', dpi=65)

def viewSetResponse():
    startData = np.zeros((200, 181))
    fig = plt.figure()
    plt.imshow(startData, origin='lower',
                extent=[-90, 90, 0, 0.2],
                aspect=500)
    plt.xlabel('Градусы')
    plt.ylabel('Время, с')
    plt.title('Набор откликов антенны в яркостном виде')
    fig.savefig('response.png', dpi=65)

def viewGridCoordinates():
    fig = plt.figure()
    xAnt = [0, 0]

    plt.plot(xAnt[0], xAnt[1], 'or', label='Антенна')
    plt.axis([-1000, 1000, 0, 1000])
    plt.xlabel('Ось, х')
    plt.ylabel('Ось, у')
    plt.title('Координаты антенны')
    plt.legend()
    plt.grid()
    fig.savefig('grid.png', dpi=65)

def startShowFigure():
    viewSignal()
    viewFilter()
    viewSetResponse()
    viewGridCoordinates()







