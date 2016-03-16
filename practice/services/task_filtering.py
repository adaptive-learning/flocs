from functools import partial


def filter_tasks_with_purchased_blocks(tasks, student):
    check_blocks = partial(requires_only_purchased_blocks, student=student)
    return list(filter(check_blocks, tasks))


def requires_only_purchased_blocks(task, student):
    required_blocks =  set(task.get_required_blocks())
    purchased_blocks =  set(student.available_blocks.all())
    return required_blocks.issubset(purchased_blocks)
