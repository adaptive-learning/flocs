import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import bokeh.plotting as bkp
from bokeh.io import gridplot

from common.flow_factors import FlowFactors


# hack to get initial difficulties (TODO: unhack)
from practice.models import TasksDifficultyModel
tasks = pd.DataFrame([dict(d.get_difficulty_dict(),
                           task=d.task.pk,
                           level=d.task.level.block_level)
                     for d in TasksDifficultyModel.objects.all()])
#tasks.to_csv('local/data/tasks-2015-04-14.csv', index=False)


def show_practice_session_plot(data_path):
    session = pd.read_csv(data_path)
    bkp.output_file("analysis/plots/simulation-last.html",
                    title="Practice simulation")
    fig = plot_practice_session(session)
    bkp.show(fig)


def show_multiple_practice_session_plots(paths, titles):
    bkp.output_file("analysis/plots/simulation-last.html",
                    title="Practice simulations")
    sessions = [pd.read_csv(path) for path in paths]
    figs = [plot_practice_session(session, title)
            for session, title in zip(sessions, titles)]
    if len(figs) % 2 == 1:
        figs += [None]
    grid = gridplot([[figs[i], figs[i+1]] for i in range(0, len(figs), 2)])
    bkp.show(grid)


def plot_practice_session(simulation, title="Practice simulation"):
    """
    Plot a practice session.

    Args:
        simulation: dataframe with simulation data
    Return:
        Bokeh figure object
    """
    proj_dif = compute_projected_difficulties(simulation)
    dif_history = proj_dif.pivot('instance', 'task', 'difficulty')
    fig = bkp.figure(title=title,
                     x_axis_label='Task instance',
                     y_axis_label='Skill / difficulty')
    # lines showing difficulties evolution
    fig.multi_line(xs=[dif_history.index.values]*len(dif_history.columns),
                   ys=[dif_history[task].values for task in dif_history],
                   color='grey', line_width=0.2)
    fig.ygrid.grid_line_color = None
    # difficulties of all tasks (and their availability)
    colormap = {True: 'black', False: 'grey'}
    colors = [colormap[x] for x in proj_dif['allowed']]
    fig.scatter(proj_dif['instance'], proj_dif['difficulty'], color=colors)
    # hack to show proper legend
    fig.scatter([], [], color='black', legend='available tasks')
    fig.scatter([], [], color='grey', legend='other tasks')
    # skill progress
    fig.line(simulation['instance'], simulation['student-STUDENT_BIAS'],
             legend="skill estimate", color='green', line_width=2)
    fig.square(simulation['instance'], simulation['student-STUDENT_BIAS'],
               legend="skill estimate", color='green')
    # difficulties and flow reports of task instances in the session
    current_difficulties = pd.merge(simulation, proj_dif,
                                    left_on=['instance', 'task-id'],
                                    right_on=['instance', 'task'])['difficulty']
    colormap = {1: 'red', 2: 'orange', 3: 'green', 4: 'blue'}
    colors = [colormap[x] for x in simulation['flow-report']]
    fig.scatter(simulation['instance'], current_difficulties,
                color=colors, marker='circle', size=10)
    # hack to show proper legend
    fig.scatter([], [], color='red', legend='given up')
    fig.scatter([], [], color='orange', legend='too difficult')
    fig.scatter([], [], color='green', legend='just right')
    fig.scatter([], [], color='blue', legend='too easy')
    fig.legend.location = 'top_left'
    return fig


def compute_projected_difficulties(simulation):
    simulation['key'] = 1
    tasks['key'] = 1
    d = pd.merge(simulation, tasks, on='key')
    d['difficulty'] = d[FlowFactors.TASK_BIAS] - \
                ( d['student-LOOPS'] * d[FlowFactors.LOOPS]\
                + d['student-CONDITIONS'] * d[FlowFactors.CONDITIONS]\
                + d['student-LOGIC_EXPR'] * d[FlowFactors.LOGIC_EXPR]\
                + d['student-COLORS'] * d[FlowFactors.COLORS]\
                + d['student-TOKENS'] * d[FlowFactors.TOKENS]\
                + d['student-PITS'] * d[FlowFactors.PITS]\
                )
    d['allowed'] = d['level_x'] >= d['level_y']
    d = d[['instance', 'task', 'difficulty', 'allowed']]
    return d
