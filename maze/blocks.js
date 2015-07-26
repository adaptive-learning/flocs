Blockly.Blocks['krok_vpred'] = {
      init: function() {
          this.appendDummyInput()
              .setAlign(Blockly.ALIGN_RIGHT)
              .appendField("krok vpřed");
          this.setPreviousStatement(true);
          this.setNextStatement(true);
          this.setColour(210);
          this.setTooltip('Provede jeden krok vpřed.');
          this.setHelpUrl('');
      }
};



Blockly.JavaScript['krok_vpred'] = function(block) {
      return 'stepForward();';
};
