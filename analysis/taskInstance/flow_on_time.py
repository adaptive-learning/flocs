import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# TODO: Create infrastructure for analysis and desribe it on our wiki.


def show_flow_on_time_plot(name, show, store):
    data = pd.read_csv('data/{name}.csv'.format(name=name))
    plot_practice_session(data)
    if store:
        plt.savefig('plots/{name}_flow_on_time.pdf'.format(name=name))
    if show:
        plt.show()


def plot_practice_session(data):
    """
    Plot a practice session (just plot, don't show or store it).

    Args:
        simulation: dataframe with simulation data
    """
    # drop attempts without flow report
    data = data[data.reported_flow != 0]

    # project only two interesting columns
    data = data.loc[:, ['reported_flow', 'time_spent']]

    data.plot(kind='scatter', x='time_spent', y='reported_flow')

    # plot style
    plt.style.use('ggplot')
    plt.ylabel('Report of the flow')
    plt.xlabel('Time spent while solving the task')
    plt.yticks([1,2,3], ('difficult', 'right', 'easy'))
    plt.ylim(0.5,3.5)
    plt.xlim(0,700)
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 10}
    plt.rc('font', **font)


if __name__ == '__main__':
    show_flow_on_time_plot('TaskInstanceModel-2015-12-15', False, True)
