"""
Model for task efficiency estimation
"""

# IDs of long tasks (boring for high-skilled students)
INEFFICIENT_TASKS = [4, 5, 6, 7, 8, 9, 10]


def estimate_efficiency(student_id, task_id, practice_context):
    """ Estimate task efficiency from practice context.

    Return:
        efficiency - real number, 1 means most efficent, 0 most inefficient
    """
    if task_id in INEFFICIENT_TASKS:
        return 0.02
    else:
        return 1.
