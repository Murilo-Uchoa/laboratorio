'''
Signal Processing Library
Sinais basicos, atraso e plotagem (biblioteca montada na Le03)
'''

import numpy as np
import matplotlib.pyplot as plt


def SIGNALgenerate(N=100, signal='delta', amplitude=1.0, phase=0.0, period=10, k=0, a=0.9, dist=None):
    '''
    N        : numero de amostras
    signal   : delta, step, exp, osc, random
    amplitude: A
    phase    : phi (osc)
    period   : M em amostras (osc)
    k        : shift (delta, step, exp)
    a        : base da exponencial
    dist     : 'uniform' para aleatorio uniforme (padrao: gaussiano)
    '''

    n = np.arange(N)
    x = np.zeros(N)

    if signal == 'delta':
        x[k] = amplitude

    if signal == 'step':
        x[k:] = amplitude

    if signal == 'exp':
        x[k:] = amplitude * np.abs(a) ** np.arange(N - k)

    if signal == 'osc':
        wo = 2 * np.pi / period
        x = amplitude * np.sin(wo * n + phase)

    if signal == 'random':
        if dist == 'uniform':
            x = amplitude * np.random.uniform(-1, 1, N)
        else:
            x = amplitude * np.random.normal(0, 1, N)

    return x, n


def SIGNALdelay(x, n):
    '''
    Slows a signal down by k samples
    '''

    result = np.zeros(len(x))
    result[n:] = x[:len(x) - n]

    return result


def SIGNALplot(x, n, titulo='', xlim=None):
    fig, ax = plt.subplots()
    ax.stem(n, x, 'r')
    ax.set_title(titulo)
    if xlim is not None:
        ax.set_xlim(xlim)
    plt.show()
