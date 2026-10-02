'''
Plot Library
Funcoes utilitarias de formatacao de graficos usadas nos notebooks do curso.
'''

import numpy as np


def figureFormat(ax, fig, tight=False):
    '''
    Aplica uma formatacao padrao (grade, layout) a uma figura.

    ax   : um Axes do matplotlib, ou um array/lista de Axes (ex: plt.subplots(2,1))
    fig  : a Figure do matplotlib correspondente
    tight: se True, aplica fig.tight_layout()
    '''
    axes = np.atleast_1d(ax).ravel()

    for a in axes:
        a.grid(True, alpha=0.3)

    if tight:
        fig.tight_layout()

    return fig, ax
