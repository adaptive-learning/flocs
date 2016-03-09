from itertools import *
from blocks.models import BlockModel
from practice.models import StudentModel


def get_next_block_for_student(student):
    """
    Returns next block which is not yet owned by the student.
    Order is given by difficulties of blocks.

    Raises NoNextBlock if the student already owns all blocks.
    """
    try:
        return next(next_blocks_for_student(student))
    except StopIteration:
        raise NoNextBlock('Student {0} already owns all blocks.'.format(student.pk))


def next_blocks_for_student(student):
    """
    Returns generator of blocks not yet owned by given student.
    Order is given by difficulties of blocks.
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


class NoNextBlock(LookupError):
    """
    Exception raised when next block is requested, but there is no next block.
    """
    pass
