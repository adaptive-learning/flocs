"""
Service for computing statistic features of the practicing.
"""

from __future__ import division
import logging

from practice.models.task_instance import TaskInstanceModel

logger = logging.getLogger(__name__)

def percentil(time, task):
    """
    Returns number in percents, which represents relative number of students,
    who solved the task equal or slower.
    """
    instances = TaskInstanceModel.objects.filter(task=task)
    times = [instance.time_spent for instance in instances]
    smaller_count = 0
    for t in times:
        if t < time:
            smaller_count += 1
    return round(100 * (smaller_count + 1)/ (len(times) + 1))

