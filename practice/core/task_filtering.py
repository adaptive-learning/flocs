"""Functions for task filtering
"""

def filter_tasks_by_level(tasks, student):
    return [task for task in tasks if level_satisfied(task, student)]


def level_satisfied(task, student):
    if not task.level or not student.level:
        return True
    return task.level <= student.level
