import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# TODO: Create infrastructure for analysis and desribe it on our wiki.

COLORS = {
    'student': 'DarkRed',
    'task': 'DarkBlue'
}


def plot_practice_simulation(name):
    simulation = pd.read_csv('data/{name}.csv'.format(name=name))

    too_difficult = simulation[simulation['flow-report'] == 1]
    just_right = simulation[simulation['flow-report'] == 2]
    too_easy = simulation[simulation['flow-report'] == 3]

    simulation = simulation.set_index('instance')
    difficulty = simulation['task-TASK_BIAS']\
            + simulation['task-LOOPS'] * simulation['task-LOOPS']\
            + simulation['task-CONDITIONS'] * simulation['task-CONDITIONS']\
            + simulation['task-LOGIC_EXPR'] * simulation['task-LOGIC_EXPR']\
            + simulation['task-COLORS'] * simulation['task-COLORS']\
            + simulation['task-TOKENS'] * simulation['task-TOKENS']\
            + simulation['task-PITS'] * simulation['task-PITS']

    plt.style.use('ggplot')
    fig, ax = plt.subplots()

    simulation['student-STUDENT_BIAS'].plot(ax=ax, kind='line',
            color=COLORS['student'], label='skill estimate')
    simulation['task-TASK_BIAS'].plot(ax=ax, kind='line',
            color=COLORS['task'], linestyle='--', label='task bias')
    difficulty.plot(ax=ax, kind='line',
            color=COLORS['task'], label='difficulty')

    difficulty.reset_index().plot(ax=ax, kind='scatter', x='instance', y=0,
            marker='o', s=50, color=COLORS['task'])
    if len(too_difficult) > 0:
        too_difficult.plot(ax=ax, kind='scatter', x='instance', y='student-STUDENT_BIAS',
                marker='v', s=100, color=COLORS['student'], label='too difficult')
    if len(just_right) > 0:
        just_right.plot(ax=ax, kind='scatter', x='instance', y='student-STUDENT_BIAS',
                marker='s', s=100, color=COLORS['student'], label='just right')
    if len(too_easy) > 0:
        too_easy.plot(ax=ax, kind='scatter', x='instance', y='student-STUDENT_BIAS',
                marker='^', s=100, color=COLORS['student'], label='too easy')

    ax.set_xlim([0.9, len(simulation) + 0.1])
    ax.set_ylim([-2, 2])
    plt.xticks(np.arange(1, len(simulation) + 1, 1))
    plt.ylabel('')
    ax.legend(loc='upper center', scatterpoints=1, ncol=2)
    plt.savefig('plots/{name}.pdf'.format(name=name))

if __name__ == '__main__':
    plot_practice_simulation('practice-simulation-stupid')
    plot_practice_simulation('practice-simulation-genius')
    plot_practice_simulation('practice-simulation-normal')
