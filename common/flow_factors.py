from enum import Enum

class FlowFactors(Enum):
    """
    Common constants to denote factors affecting flow
    """
    STUDENT_BIAS    = 0
    TASK_BIAS       = 1
    LOOPS           = 2
    CONDITIONS      = 3
    LOGIC_EXPR      = 4
    COLORS          = 5
    TOKENS          = 6
    PITS            = 7


    @classmethod
    def game_factors(cls):
        return [cls.COLORS, cls.TOKENS, cls.PITS]

    @classmethod
    def concept_factors(cls):
        return [cls.LOOPS, cls.CONDITIONS, cls.LOGIC_EXPR]

    @classmethod
    def student_factors(cls):
        return [cls.STUDENT_BIAS] + cls.concept_factors() + cls.game_factors()

    @classmethod
    def task_factors(cls):
        return [cls.TASK_BIAS] + cls.concept_factors() + cls.game_factors()

