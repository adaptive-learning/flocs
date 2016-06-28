from collections import namedtuple
from practice.models import StudentModel
from blocks.models import Toolbox

ProgressLevel = namedtuple('ProgressLevel',
        ['level', 'credits_from', 'credits_to', 'max_credits', 'blocks'])
Level = namedtuple('Level',
        ['level', 'max_credits', 'blocks'])

def level_progress(student, new_credits):
    credits_from = student.free_credits
    student.earn_credits(new_credits)
    progress = []
    success = True
    while success:
        acquiring_level = find_acquiring_level(student)
        progress_info, success = progress_within_level(student, acquiring_level, credits_from)
        progress.append(progress_info)
        credits_from = 0
    return progress


def progress_within_level(student, level, credits_from):
    """ Make progress withing level.

    Return:
        - info about progress achieved (ProgressLevel)
        - whether next level was achieved (bool)
    """
    success = student.free_credits >= level.max_credits
    credits_to = min(level.max_credits, student.free_credits)
    if success:
        try:
            levelup(student)
        except NoNextLevel:
            # if there is no next level, then just spend credits
            student.spend_credits(level.max_credits)
    progress_info = ProgressLevel(
        level=level.level,
        credits_from=credits_from,
        credits_to=credits_to,
        max_credits=level.max_credits,
        blocks=level.blocks if success else [])
    return progress_info, success


def find_acquiring_level(student):
    next_toolbox = Toolbox.objects.get_next(student.toolbox)
    level = student.toolbox.level
    if not next_toolbox:
        return Level(level=level, max_credits=1000, blocks=[])
    acquiring_level =  Level(level=level, max_credits=next_toolbox.credits,
                             blocks=next_toolbox.get_new_blocks())
    return acquiring_level





def levelup(student):
    """ Move student to next level.
        Raise LevelupNotPossible if it's not possible.
    """
    if not student.toolbox:
        raise LevelupNotPossible(
                'Student {s} does not have assigned toolbox.'
                .format(s=student.pk))
    next_toolbox = Toolbox.objects.get_next(student.toolbox)
    if not next_toolbox:
        raise NoNextLevel(
                'Student {s} already has full toolbox.'
                .format(s=student.pk))
    try:
        student.spend_credits(next_toolbox.credits)
        student.toolbox = next_toolbox
        student.save()
    except ValueError:
        raise LevelupNotPossible(
                'Student {s} does not have enough credits for next toolbox.'
                .format(s=student.pk))


class LevelupNotPossible(ValueError):
    """Exception raised when levelup is tried, but is denied.
    """
    pass

class NoNextLevel(LevelupNotPossible):
    """Exception raised when there is no next level to acquire
    """
    pass

