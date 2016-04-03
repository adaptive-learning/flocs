from practice.models import StudentModel
from levels.models import Level


def try_levelup(student):
    """
    If student has enough credits for next level, increase her level.

    Return:
        whether next level was achived (bool)
    """
    try:
        levelup(student)
        return True
    except LevelupNotPossible:
        return False


def levelup(student):
    """Move student to next level, raises LevelupNotPossible if it's not possible.
    """
    if not student.level:
        raise LevelupNotPossible(
                'Student {s} does not have assigned level.'
                .format(s=student.pk))
    next_level = Level.objects.next_level(student.level)
    if not next_level:
        raise LevelupNotPossible(
                'Student {s} has already achieved maximum level.'
                .format(s=student.pk))
    try:
        student.spend_credits(next_level.credits)
        student.level = next_level
        student.save()
    except ValueError:
        raise LevelupNotPossible(
                'Student {s} does not have enough credits for next level.'
                .format(s=student.pk))


class LevelupNotPossible(ValueError):
    """Exception raised when levelup is tried, but is denied.
    """
    pass
