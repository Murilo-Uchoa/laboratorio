# Laboratórios - INF0413 Processamento Digital de Sinais

**Aluno:** Murilo Uchoa
**Turma:** 2026-2 - UFG

| Pasta | Atividade |
|-------|-----------|
| `le03_discrete-time-signals/` | Lecture 3 - Sinais de tempo discreto: biblioteca de sinais básicos (delta, degrau, senoide, exponencial, aleatório) |
| `le04_karplus-strong/` | Lecture 4 - Reconstrução de sinais: seno e periódico aleatório com frequência e duração controladas, plots em amostras e no tempo |

## Como rodar

Cada pasta tem o notebook e uma `lib/` com as funções auxiliares. Abra o Jupyter
de dentro da pasta da atividade para os imports funcionarem:

```bash
cd le03_discrete-time-signals
jupyter lab
```

Dependências: `numpy`, `matplotlib`, `jupyterlab`, `music21` (usada pela `lib/myAudioProcessingLib.py` para tocar áudio e MIDI).
