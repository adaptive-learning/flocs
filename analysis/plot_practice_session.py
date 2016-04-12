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
    too_difficult = simulation[simulation['flow-report'] == 2]
    just_right = simulation[simulation['flow-report'] == 3]
    too_easy = simulation[simulation['flow-report'] == 4]

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


def index_scatter(ax, df, y, marker, label):
    if len(df) > 0:
        df.reset_index().plot(ax=ax, kind='scatter',
                x='index', y=y,
                marker=marker,
                s=100, color=COLORS['task'],
                label=label)


def plot_practice_session_from_real_data(student=15):
    # load data
    # TODO: use paths to versioned data
    taskinstances = pd.read_csv('data/TaskInstanceModel-2015-12-15.csv')
    tasks = pd.read_csv('data/TasksDifficultyModel-2015-12-15.csv')
    students = pd.read_csv('data/StudentsSkillModel-2015-12-15.csv')
    skills = list(students.set_index('student').loc[student])

    # prepare data
    session = taskinstances[taskinstances.student == student]
    session = session.sort_values(by='time_start')
    session = pd.merge(session, tasks)
    too_difficult = session[session['reported_flow'] == 1]
    just_right = session[session['reported_flow'] == 2]
    too_easy = session[session['reported_flow'] == 3]

    with_report_count = len(too_difficult) + len(just_right) + len(too_easy)
    if with_report_count < 7:
        print('Too few data for student ', student)
        return

    # plot
    plt.style.use('ggplot')
    fig, ax = plt.subplots()

    session['programming'].plot(ax=ax, kind='line',
            color=COLORS['task'], label='difficulty')
    index_scatter(ax, too_difficult, 'programming', 'v', 'too difficult')
    index_scatter(ax, just_right, 'programming', 's', 'just right')
    index_scatter(ax, too_easy, 'programming', '^', 'too easy')

    ax.set_xlim([-0.1, len(session) - 0.9])
    ax.set_ylim([-2, 2])
    plt.xticks(np.arange(0, len(session), 1))
    plt.ylabel('difficulty')
    plt.figtext(0.01, .01, r"skill: $\beta = {beta:.1f}$, $\alpha = {alpha}$"\
            .format(beta=skills[0], alpha=tuple(map(int, skills[1:]))),
        fontdict={'size': 14})
    ax.legend(loc='upper center', scatterpoints=1, ncol=2)
    fig.tight_layout()
    plt.show()
    #plt.savefig('plots/student-{student}.pdf'.format(student=student))


if __name__ == '__main__':
    store_practice_session_plot('practice-simulation-stupid')
    store_practice_session_plot('practice-simulation-genius')
    store_practice_session_plot('practice-simulation-normal')
