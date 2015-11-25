"""
Model for instruction that are shown to user in case he deals with new (or not
yet mastered) concept.
"""
from django.db import models
from common.flow_factors import FlowFactors

class InstructionsModel(models.Model):
    """
    Represents the instruction messages that are shown to the user when dealing
    with new concept.
    """
    
    GENERAL_COMMENT = 255

    FLOWS_FACTOR_VALUES = (
        (GENERAL_COMMENT,                          'instructions on basics of the game'),
        (FlowFactors.LOGIC_EXPR.value, 'instructions conserning logical expresions'),
        (FlowFactors.COLORS.value,     'instructions conserning colors'),
        (FlowFactors.TOKENS.value,     'instructions conserning tokens'),
        (FlowFactors.PITS.value,       'instructions conserning pits'),
        (FlowFactors.LOOPS.value,      'instructions conserning loops'),
        (FlowFactors.CONDITIONS.value, 'instructions on how to use conditions')
    )

    # with which factor are these instructions tied
    flow_factor = models.SmallIntegerField(
        choices=FLOWS_FACTOR_VALUES,
        default=GENERAL_COMMENT,
        verbose_name="Factor to which these instructions belong"
    )

    # test of instruction itself
    text = models.CharField(
        max_length=255,
        verbose_name="Text of instruction shown in game page"
    )

    def __str__(self):
        templ = 'flow_factor={flow_factor}, text={text}'
        return templ.format(
            flow_factor=self.flow_factor,
            text=self.text
        )

    def get_flow_factor(self):
        """
        Getter for flow factor.
        """
        if self.flow_factor == self.GENERAL_COMMENT:
            return self.GENERAL_COMMENT
        else:
            return FlowFactors(self.flow_factor)

    def get_text(self):
        """
        Getter for textual instructions.
        """
        return self.text
