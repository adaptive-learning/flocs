from practice.models import StudentModel
from blocks.models import Toolbox


def try_levelup(student):
    """ If student has enough credits for next level, increase her level.

    Return:
        whether next level was achived (bool)
    """
    try:
        levelup(student)
        return True
    except LevelupNotPossible:
        return False


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
        raise LevelupNotPossible(
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
