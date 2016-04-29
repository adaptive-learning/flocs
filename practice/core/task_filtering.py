"""Functions for task filtering
"""

def filter_tasks_by_level(tasks, student):
    return [task for task in tasks if level_satisfied(task, student)]


def level_satisfied(task, student):
    if not task.toolbox or not student.toolbox:
        return True
    return task.toolbox.level <= student.toolbox.level
