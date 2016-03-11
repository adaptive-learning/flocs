from itertools import *
from blocks.models import BlockModel
from practice.models import StudentModel


def get_next_purchasable_block(student):
    """
    Returns next block not yet owned by student, but only if the student can
    afford to buy this block. Otherwise returns None.
    """
    try:
        next_block = get_next_block_for_student(student)
        if student.free_credits >= next_block.price:
            return next_block
        else:
            return None
    except NoNextBlockException:
        return None


def get_next_block_for_student(student):
    """
    Returns next block which is not yet owned by the student.
    Order is given by difficulties of blocks.

    Raises NoNextBlockException if the student already owns all blocks.
    """
    try:
        return next(next_blocks_for_student(student))
    except StopIteration:
        raise NoNextBlockException('Student {0} already owns all blocks.'.format(student.pk))


def next_purchasable_blocks(student):
    """
    Generator of blocks which the student doesn't own and can afford to buy
    """
    return next_blocks_for_student(student)



def next_blocks_for_student(student):
    """
    Generator of blocks not yet owned by given student

    Yields:
        blocks not owned by the student in order given by their difficulties
    """
    all_blocks_ordered = BlockModel.objects.all_ordered()
    owned_blocks_ordered = chain(student.available_blocks.all_ordered(),
                                 repeat(None))
    cheapest_owned_block = next(owned_blocks_ordered)
    for block in all_blocks_ordered:
        if block == cheapest_owned_block:
            cheapest_owned_block = next(owned_blocks_ordered)
        else:
            yield block


class NoNextBlockException(LookupError):
    """
    Exception raised when next block is requested, but there is no next block.
    """
    pass
