from blocks.models import BlockModel
from practice.models import StudentModel


def buy_block(student, block):
    """
    Adds requested block to the student and deduces credits from his account.

    Raises:
        ValueError - if student already owns this block
        NotEnoughtCreditsException - if the student does not have enought
                                     credits to buy the block
    """
    if student.available_blocks.filter(pk=block.pk).exists():
        raise ValueError(
                'Student {s} already owns block {b}.'
                .format(s=student.pk, b=block))
    try:
        student.spend_credits(block.price)
    except ValueError:
        raise NotEnoughtCreditsException(
                'Student {s} does not have enough credits to buy block {b}.'
                .format(s=student.pk, b=block))
    student.available_blocks.add(block)
    student.save()  # necessary (to save changed credits)


class NotEnoughtCreditsException(ValueError):
    """
    Exception raised when an operation requires more credits than how many are
    available
    """
    pass
