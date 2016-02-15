"""
service for obtaining statistical type of data about tasks and their instances.
"""

import logging
from practice.models import TaskInstanceModel

logger = logging.getLogger(__name__)

def get_solved_tasks_count(student):
    """
    Returns number of successfully solved tasks by the given user.
    
    Args:
        student: student to whom we search solved tasks

    Returns:
        number of solved tasks

    Raises:
        ValueError: If the student argument is None.
    """
    logger.info("Getting number of solved tasks for student with id %s",
                student.id)
    if not student:
        raise ValueError("Student is required for get_solved_tasks_count")

    return TaskInstanceModel.objects.filter(student=student, solved=True)

def get_solved_distinct_tasks_count(student):
    """
    Returns number of successfully solved distinct tasks by the given user.
    
    Args:
        student: student to whom we search solved tasks

    Returns:
        number of solved distict tasks (more instances of the same task are
        counted as one)

    Raises:
        ValueError: If the student argument is None.
    """
    logger.info("Getting number of solved tasks for student with id %s",
                student.id)
    if not student:
        raise ValueError("Student is required for get_solved_tasks_count")

    return TaskInstanceModel.objects.filter(
        student=student, solved=True).values('task').distinct()
