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

Blockly.Blocks['krok_vzad'] = {
      init: function() {
          this.appendDummyInput()
              .setAlign(Blockly.ALIGN_RIGHT)
              .appendField("krok vzad");
          this.setPreviousStatement(true);
          this.setNextStatement(true);
          this.setColour(210);
          this.setTooltip('Provede jeden krok vzad.');
          this.setHelpUrl('');
      }
};



Blockly.JavaScript['krok_vzad'] = function(block) {
      return 'stepBackward();';
};

Blockly.Blocks['je_cesta_vlevo'] = {
      init: function() {
          this.appendDummyInput()
              .setAlign(Blockly.ALIGN_RIGHT)
              .appendField("je cesta vlevo");
          this.setOutput(true);
          this.setColour(210);
          this.setTooltip('Zkontroluje, zda je vlevo volná cesta.');
          this.setHelpUrl('');
      }
};



Blockly.JavaScript['je_cesta_vlevo'] = function(block) {
    var code = 'eval(checkLeft())';
    return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.Blocks['je_cesta_vpravo'] = {
      init: function() {
          this.appendDummyInput()
              .setAlign(Blockly.ALIGN_RIGHT)
              .appendField("je cesta vpravo");
          this.setOutput(true);
          this.setColour(210);
          this.setTooltip('Zkontroluje, zda je vpravo volná cesta.');
          this.setHelpUrl('');
      }
};



Blockly.JavaScript['je_cesta_vpravo'] = function(block) {
    var code = 'eval(checkRight())';
    return [code, Blockly.JavaScript.ORDER_FUNCTION_CALL];
};

Blockly.Blocks['otocit_vlevo'] = {
      init: function() {
          this.appendDummyInput()
              .setAlign(Blockly.ALIGN_RIGHT)
              .appendField("otočit vlevo");
          this.setPreviousStatement(true);
          this.setNextStatement(true);
          this.setColour(210);
          this.setTooltip('Provede otočku o 90° vlevo.');
          this.setHelpUrl('');
      }
};



Blockly.JavaScript['otocit_vlevo'] = function(block) {
      return 'turnLeft();';
};

Blockly.Blocks['otocit_vpravo'] = {
      init: function() {
          this.appendDummyInput()
              .setAlign(Blockly.ALIGN_RIGHT)
              .appendField("otočit vpravo");
          this.setPreviousStatement(true);
          this.setNextStatement(true);
          this.setColour(210);
          this.setTooltip('Provede otočku o 90° vpravo.');
          this.setHelpUrl('');
      }
};



Blockly.JavaScript['otocit_vpravo'] = function(block) {
      return 'turnRight();';
};

Blockly.Blocks['if_then'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("pokud");
    this.appendValueInput("condition")
        .setCheck("Boolean")
        .setAlign(Blockly.ALIGN_CENTRE);
    this.appendDummyInput()
        .appendField("pak");
    this.appendStatementInput("condition_true");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(330);
    this.setTooltip('Vykoná příkaz, pokud je splněna podmínka.');
  }
};

Blockly.JavaScript['if_then'] = function(block) {
  var value_condition = Blockly.JavaScript.valueToCode(block, 'condition', Blockly.JavaScript.ORDER_ATOMIC);
  var statements_condition_true = Blockly.JavaScript.statementToCode(block, 'condition_true');
  var code = "if (" + value_condition + ") {" + statements_condition_true + "}";
  return code;
};

Blockly.Blocks['if_then_else'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("pokud");
    this.appendValueInput("condition")
        .setCheck("Boolean")
        .setAlign(Blockly.ALIGN_CENTRE);
    this.appendDummyInput()
        .appendField("pak");
    this.appendStatementInput("condition_true");
    this.appendDummyInput()
        .appendField("jinak");
    this.appendStatementInput("condition_false");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(330);
    this.setTooltip('Vykoná různé příkazy podle toho, zda je splněna podmínka.');
  }
};

Blockly.JavaScript['if_then_else'] = function(block) {
  var value_condition = Blockly.JavaScript.valueToCode(block, 'condition', Blockly.JavaScript.ORDER_ATOMIC);
  var statements_condition_true = Blockly.JavaScript.statementToCode(block, 'condition_true');
  var statements_condition_false = Blockly.JavaScript.statementToCode(block, 'condition_false');
  var code = "if (" + value_condition + ") {" + statements_condition_true + "} else {" + statements_condition_false + "}";
  return code;
};
