import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# TODO: Create infrastructure for analysis and desribe it on our wiki.

COLORS = {
    'student': 'DarkRed',
    'task': 'DarkBlue'
}


def store_practice_session_plot(name):
    """
    NOTE: For now, this function is limited to be run from analysis directory.
    """
    session = pd.read_csv('data/{name}.csv'.format(name=name))
    plot_practice_session(session)
    plt.savefig('plots/{name}.pdf'.format(name=name))


def show_practice_session_plot(data_path):
    session = pd.read_csv(data_path)
    plot_practice_session(session)
    plt.show()


def plot_practice_session(simulation):
    """
    Plot a practice session (just plot, don't show or store it).

    Args:
        simulation: dataframe with simulation data
    """
    too_difficult = simulation[simulation['flow-report'] == 1]
    just_right = simulation[simulation['flow-report'] == 2]
    too_easy = simulation[simulation['flow-report'] == 3]

    simulation = simulation.set_index('instance')
    difficulty = simulation['task-TASK_BIAS'] -\
            ( simulation['student-LOOPS'] * simulation['task-LOOPS']\
            + simulation['student-CONDITIONS'] * simulation['task-CONDITIONS']\
            + simulation['student-LOGIC_EXPR'] * simulation['task-LOGIC_EXPR']\
            + simulation['student-COLORS'] * simulation['task-COLORS']\
            + simulation['student-TOKENS'] * simulation['task-TOKENS']\
            + simulation['student-PITS'] * simulation['task-PITS']\
            )

    plt.style.use('ggplot')
    fig, ax = plt.subplots()

    simulation['student-STUDENT_BIAS'].plot(ax=ax, kind='line',
            color=COLORS['student'], label='skill estimate')
    difficulty.plot(ax=ax, kind='line',
            color=COLORS['task'], label='difficulty', marker='o')
    #difficulty.reset_index().plot(ax=ax, kind='scatter', x='instance', y=0,
    #        marker='o', s=50, color=COLORS['task'])

    simulation.reset_index().plot(ax=ax, kind='scatter', label='task bias',
            x='instance', y='task-TASK_BIAS',
            color=COLORS['task'], s=70, marker='+')

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
    fig.tight_layout()


if __name__ == '__main__':
    store_practice_session_plot('practice-simulation-stupid')
    store_practice_session_plot('practice-simulation-genius')
    store_practice_session_plot('practice-simulation-normal')
