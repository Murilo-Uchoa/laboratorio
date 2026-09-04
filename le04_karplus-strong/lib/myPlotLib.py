'''
Plot Library
Reconstruida a partir do uso nos notebooks da disciplina INF0413
(o repositorio original nao inclui este arquivo).
'''

import numpy as np
import matplotlib.pyplot as plt


def figureFormat(ax, fig=None, tight=False, grid=True, xlabel=None, ylabel=None, title=None):
    '''
    Formata um ou varios eixos do matplotlib com um visual limpo.

    ax     : eixo (matplotlib.axes.Axes) ou array de eixos (plt.subplots(2, 1))
    fig    : figura (matplotlib.figure.Figure), opcional
    tight  : aplica fig.tight_layout()
    grid   : mostra a grade
    xlabel : rotulo do eixo x
    ylabel : rotulo do eixo y
    title  : titulo do grafico
    '''
    axes = np.atleast_1d(ax).ravel() if isinstance(ax, (list, tuple, np.ndarray)) else [ax]

    for a in axes:
        a.spines['top'].set_visible(False)
        a.spines['right'].set_visible(False)
        a.tick_params(axis='both', labelsize=10)
        if grid:
            a.grid(True, linestyle=':', alpha=0.6)
        if xlabel is not None:
            a.set_xlabel(xlabel)
        if ylabel is not None:
            a.set_ylabel(ylabel)
        if title is not None:
            a.set_title(title)

    if fig is None:
        fig = axes[0].figure
    if tight:
        fig.tight_layout()

    return ax
