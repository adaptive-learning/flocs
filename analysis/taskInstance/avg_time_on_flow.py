import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# TODO: Create infrastructure for analysis and desribe it on our wiki.


def show_flow_on_time_plot(name, show, store):
    data = pd.read_csv('data/{name}.csv'.format(name=name))
    plot_practice_session(data)
    if store:
        plt.savefig('plots/{name}_avg_time_on_flow.pdf'.format(name=name))
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

    
    difficulty = data[data.reported_flow == 1]
    right = data[data.reported_flow == 2]
    easy = data[data.reported_flow == 3]
    
    means = [difficulty.mean()[1], right.mean()[1], easy.mean()[1]]

    plt.bar([1,2,3], means, 0.5)

    # plot style
    plt.style.use('ggplot')
    plt.ylabel('Average time [sec]')
    plt.xlabel('Reported flow')
    plt.xticks([1.25,2.25,3.25], ('difficult', 'right', 'easy'))
    plt.ylim(0,700)
    plt.xlim(0.5,4)
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 10}
    plt.rc('font', **font)


if __name__ == '__main__':
    show_flow_on_time_plot('TaskInstanceModel-2015-12-15', False, True)
