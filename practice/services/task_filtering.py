from functools import partial


def filter_tasks_with_purchased_blocks(tasks, student):
    purchased_blocks =  set(student.get_available_blocks())
    return [task for task in tasks
            if set(task.get_required_blocks()).issubset(purchased_blocks)]
