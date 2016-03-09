from itertools import chain
from blocks.models import BlockModel
from practice.models import StudentModel


def get_next_block_for_student(student):
    """
    Returns next block (in order given by blocks' difficulties) which is not
    yet owned by the student
    """
    all_ordered_blocks = BlockModel.objects.all_ordered()
    students_ordered_blocks = student.available_blocks.all_ordered()
    for possible_block, students_block in zip(all_ordered_blocks,
                                              chain(students_ordered_blocks, [None])):
        if possible_block != students_block:
            return possible_block
