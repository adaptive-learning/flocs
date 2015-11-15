from enum import Enum

class FlowFactor(Enum):
    """
    Common constants to denote factors affecting flow
    """
    STUDENT_BIAS    = 0
    TASK_BIAS       = 1
    LOOPS           = 2
    CONDITIONS      = 3
    LOGIC_EXPR      = 4
    COLORS          = 5
    PITS            = 6
    TOOLS           = 7


    @classmethod
    def game_factors(cls):
        return [cls.COLORS, cls.PITS, cls.TOOLS]

    @classmethod
    def concept_factors(cls):
        return [cls.LOOPS, cls.CONDITIONS, cls.LOGIC_EXPR]

