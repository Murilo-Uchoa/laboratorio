'''
Signal Processing Library
Sinais basicos, atraso e plotagem - INF0413 Processamento Digital de Sinais
Biblioteca montada na Le03 - Murilo Uchoa

Uso:
    from lib.mySignalProcessingLib import *

    x, n = SIGNALgenerate(30, 'delta', k=4)
    SIGNALplot(x, n, 'delta')

    xd = SIGNALdelay(x, 5)        # o 2o argumento e o atraso, nao o vetor n
'''

import numpy as np
import matplotlib.pyplot as plt

SIGNALS = ('delta', 'step', 'exp', 'osc', 'random')


def _format(ax, fig):
    '''
    Usa o figureFormat do myPlotLib se ele estiver por perto;
    se nao estiver, formata no basico (a lib nao depende dele).
    '''
    figureFormat = None
    try:
        from .myPlotLib import figureFormat          # lib/ importada como pacote
    except ImportError:
        try:
            from myPlotLib import figureFormat       # myPlotLib.py solto no path
        except ImportError:
            pass

    if figureFormat is not None:
        figureFormat(ax, fig, tight=True)
        return

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, linestyle=':', alpha=0.6)
    fig.tight_layout()


def SIGNALgenerate(N=100, signal='delta', amplitude=1.0, phase=0.0,
                   period=10, k=0, a=0.9, dist=None,
                   A=None, phi=None, P=None):
    '''
    Gera um sinal basico de N amostras. Devolve a tupla (x, n).

    N        : numero de amostras
    signal   : 'delta', 'step', 'exp', 'osc' ou 'random'
    amplitude: A, escala do sinal
    phase    : phi em radianos (so 'osc')
    period   : P em amostras (so 'osc') -> frequencia digital wo = 2*pi/P
    k        : shift em amostras (delta, step, exp).
               NAO se aplica a 'osc': para deslocar a senoide use 'phase'
               (phi = -2*pi*k/P), ou atrase de verdade com SIGNALdelay(x, k).
    a        : base da exponencial (|a| < 1 decai, |a| > 1 cresce)
    dist     : 'uniform' para aleatorio uniforme em [-1, 1] (padrao: gaussiano)

    Apelidos da notacao da disciplina - A sin(wo n + phi), com wo = 2 pi / P:
      A = amplitude, phi = phase, P = period
    Os dois nomes funcionam; se voce passar os dois, o apelido vence.

    Exemplos:
        x, n = SIGNALgenerate(30, 'delta', k=4)          # d[n-4]
        x, n = SIGNALgenerate(30, 'step',  k=4)          # u[n-4]
        x, n = SIGNALgenerate(30, 'exp',   a=0.8)        # 0.8^n u[n]
        x, n = SIGNALgenerate(40, 'osc',   period=15)    # sin(2 pi n / 15)
        x, n = SIGNALgenerate(40, 'osc',   P=10, phi=np.pi/2)  # = cosseno
        x, n = SIGNALgenerate(50, 'random', dist='uniform')
    '''
    if A is not None:                  # A sin(wo n + phi)
        amplitude = A
    if phi is not None:
        phase = phi
    if P is not None:                  # wo = 2 pi / P
        period = P

    if signal not in SIGNALS:
        raise ValueError(
            f'signal={signal!r} nao existe. Use um de: ' + ', '.join(SIGNALS))

    N = int(N)
    if N <= 0:
        raise ValueError(f'N={N}: o sinal precisa de pelo menos 1 amostra')

    n = np.arange(N)
    x = np.zeros(N)

    if signal in ('delta', 'step', 'exp') and not 0 <= k < N:
        raise ValueError(
            f'k={k} cai fora do sinal: precisa estar entre 0 e N-1 (N={N})')

    if signal == 'delta':
        # Delta (impulse): d[n - k]
        x[k] = amplitude

    elif signal == 'step':
        # Step: u[n - k] - liga em k e nao desliga mais
        x[k:] = amplitude

    elif signal == 'exp':
        # Exponential: |a|^(n-k) u[n-k] - o expoente conta de 0 a partir de k,
        # entao o sinal sempre "liga" valendo amplitude e dai decai
        x[k:] = amplitude * np.abs(a) ** np.arange(N - k)

    elif signal == 'osc':
        # Oscillation: A sin(wo n + phi), com wo = 2 pi / P
        if period == 0:
            raise ValueError('period=0: a senoide precisa de periodo != 0')
        wo = 2 * np.pi / period
        x = amplitude * np.sin(wo * n + phase)

    elif signal == 'random':
        if dist == 'uniform':
            x = amplitude * np.random.uniform(-1, 1, N)   # uniforme em [-1, 1]
        else:
            x = amplitude * np.random.normal(0, 1, N)     # gaussiano N(0, 1)

    return x, n


def SIGNALdelay(x, k):
    '''
    Atrasa o sinal x em k amostras: devolve x[n - k], com zeros no comeco
    e cortando o que sai pelo fim.

    Atencao: o segundo argumento e o ATRASO (um inteiro), e nao o vetor de
    amostras que o SIGNALgenerate devolve. Depois de

        x, n = SIGNALgenerate(20, 'delta')

    o certo e SIGNALdelay(x, 5), nunca SIGNALdelay(x, n).
    '''
    x = np.asarray(x)

    if np.ndim(k) != 0:
        raise TypeError(
            'SIGNALdelay(x, k): k e o atraso em amostras (um inteiro), nao o '
            'vetor n do SIGNALgenerate. Ex.: SIGNALdelay(x, 5)')

    k = int(k)
    if not 0 <= k <= len(x):
        raise ValueError(
            f'k={k} fora do intervalo: o atraso vai de 0 a {len(x)} amostras')

    result = np.zeros(len(x))
    result[k:] = x[:len(x) - k]

    return result


def SIGNALplot(x, n=None, titulo='', fmt='r'):
    '''
    Plota o sinal em stem (amostras isoladas, que e o que um sinal
    discreto e de fato).

    x     : o sinal
    n     : vetor de amostras. Pode ser omitido -> usa 0, 1, ..., len(x)-1
    titulo: titulo do grafico
    fmt   : cor/estilo das hastes ('r', 'b', 'g:', ...)

    Devolve (fig, ax), caso voce queira mexer no grafico depois.
    '''
    x = np.asarray(x)
    if n is None:
        n = np.arange(len(x))
    n = np.asarray(n)

    if len(n) != len(x):
        raise ValueError(
            f'n e x tem tamanhos diferentes: len(n)={len(n)}, len(x)={len(x)}')

    fig, ax = plt.subplots()
    ax.stem(n, x, fmt)
    ax.set_xlabel('n (amostras)')
    ax.set_ylabel('x[n]')
    if titulo:
        ax.set_title(titulo)
    _format(ax, fig)
    plt.show()

    return fig, ax
