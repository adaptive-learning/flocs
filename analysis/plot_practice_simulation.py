import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# NOTE: This is just a quick and dirty try of plotting
# TODO: Make it nice, readable and extensible, create infrastructure for
# analysis and desribe it on our wiki.

plt.style.use('ggplot')
df = pd.read_csv('data/practice-simulation-stupid.csv')
df['student-STUDENT_BIAS'].plot(kind='line', y='student-STUDENT_BIAS', marker='s')
df['task-TASK_BIAS'].plot(kind='line', y='task-TASK_BIAS', marker='o')

plt.savefig('plots/practice-simulation-stupid.pdf', bbox_inches='tight')
