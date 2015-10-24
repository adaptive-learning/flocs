/*
 * Blockly Service
 */
angular.module('flocs.workspace')
.factory('blocklyService', [function() {

  /**
  * Blockly initialization (blocks description).
  */
  function initializeBlockly() {
    // TODO(?): move blocksList to a separate blocksService
    var blocksList = [
      {
        "id": "maze_move_forward",
        "lastDummyAlign0": "LEFT",
        "message0": "krok vpred",
        "args0": [],
        "previousStatement": true,
        "nextStatement": true,
        "colour": 120,
        "tooltip": "",
        "helpUrl": ""
      },
      {
        "id": "maze_move_backward",
        "lastDummyAlign0": "LEFT",
        "message0": "krok vzad",
        "args0": [],
        "previousStatement": true,
        "nextStatement": true,
        "colour": 120,
        "tooltip": "",
        "helpUrl": ""
      },
      {
        "id": "maze_turn_left",
        "lastDummyAlign0": "LEFT",
        "message0": "zatoc doleva",
        "args0": [],
        "previousStatement": true,
        "nextStatement": true,
        "colour": 120,
        "tooltip": "",
        "helpUrl": ""
      },
      {
        "id": "maze_turn_right",
        "lastDummyAlign0": "LEFT",
        "message0": "zatoc doprava",
        "args0": [],
        "previousStatement": true,
        "nextStatement": true,
        "colour": 120,
        "tooltip": "",
        "helpUrl": ""
      },
      {
        "id": "maze_check_path_left",
        "lastDummyAlign0": "LEFT",
        "message0": "je cesta vlevo",
        "output": "Boolean",
        "colour": 210,
        "tooltip": "",
        "helpUrl": ""
      },
      {
        "id": "maze_check_path_right",
        "lastDummyAlign0": "LEFT",
        "message0": "je cesta vpravo",
        "output": "Boolean",
        "colour": 210,
        "tooltip": "",
        "helpUrl": ""
      },
      {
        "id": "maze_check_path_front",
        "lastDummyAlign0": "LEFT",
        "message0": "je cesta vpředu",
        "output": "Boolean",
        "colour": 210,
        "tooltip": "",
        "helpUrl": ""
      },

      {
        "id": "if_then",
        "message0": "pokud %1 %2 pak %3 %4",
        "args0": [
        {
            "type": "input_dummy"
        },
        {
            "type": "input_value",
            "name": "condition",
            "check": "Boolean"
        },
        {
            "type": "input_dummy"
        },
        {
            "type": "input_statement",
            "name": "condition_true"
        }
        ],
        "previousStatement": null,
        "nextStatement": null,
        "colour": 330,
        "tooltip": "",
        "helpUrl": ""
      },
      {
        "id": "if_then_else",
        "message0": "pokud %1 %2 pak %3 %4 jinak %5 %6",
        "args0": [
        {
            "type": "input_dummy"
        },
        {
            "type": "input_value",
            "name": "condition",
            "check": "Boolean"
        },
        {
            "type": "input_dummy"
        },
        {
            "type": "input_statement",
            "name": "condition_true"
        },
        {
            "type": "input_dummy"
        },
        {
            "type": "input_statement",
            "name": "condition_false"
        }
        ],
        "previousStatement": null,
        "nextStatement": null,
        "colour": 330,
        "tooltip": "",
        "helpUrl": ""
      },
      {
        "id": "for_loop_fixed",
        "message0": "opakuj %1 krát %2 %3",
        "args0": [
        {
            "type": "field_input",
            "name": "times",
            "text": "10"
        },
        
        {
            "type": "input_dummy"
        },
        {
            "type": "input_statement",
            "name": "body"
        }
        ],
        "previousStatement": null,
        "nextStatement": null,
        "colour": 120,
        "tooltip": "",
        "helpUrl": ""
      },
      {
        "id": "for_loop",
        "message0": "pro i od %1 do %2 opakuj %3 %4",
        "args0": [
        {
            "type": "field_input",
            "name": "from",
            "text": "1"
        },
        {
            "type": "field_input",
            "name": "to",
            "text": "10"
        },

        {
            "type": "input_dummy"
        },
        {
            "type": "input_statement",
            "name": "body"
        }
        ],
        "previousStatement": null,
        "nextStatement": null,
        "colour": 120,
        "tooltip": "Pro všechny hodnoty proměnné i od počáteční do koncové " +
            "včetně bude opakovat vnořené příkazy.",
        "helpUrl": ""
      },


      {
        "id": "while_loop",
        "message0": "dokud platí, že %1 pak vykonávej %2 %3",
        "args0": [ 
        {
            "type": "input_value",
            "name": "condition",
            "check": "Boolean"
        },
        {
            "type": "input_dummy"
        },
        {
            "type": "input_statement",
            "name": "body"
        }
        ],
        "previousStatement": null,
        "nextStatement": null,
        "colour": 120,
        "tooltip": "",
        "helpUrl": ""
      }
    ];

    // load all blocks
    function initBlock(jsonBlock) {
      return function() {
        this.jsonInit(jsonBlock);
      };
    }
    for (var i = 0; i < blocksList.length; i++) {
      var jsonBlock = blocksList[i];
      Blockly.Blocks[jsonBlock.id] = {
        init: initBlock(jsonBlock)
      };
    }

    Blockly.JavaScript['maze_move_forward'] = function(block) {
      return 'moveForward();';
    };
    Blockly.JavaScript['maze_turn_left'] = function(block) {
      return 'turnLeft();';
    };
    Blockly.JavaScript['maze_turn_right'] = function(block) {
      return 'turnRight();';
    };

    Blockly.JavaScript['maze_move_backward'] = function(block) {
      return 'moveBackward();';
    };

    Blockly.JavaScript['maze_check_path_left'] = function(block) {
      return 'checkPathLeft()';
    };

    Blockly.JavaScript['maze_check_path_right'] = function(block) {
      return 'checkPathRight()';
    };

    Blockly.JavaScript['maze_check_path_front'] = function(block) {
      return 'checkPathFront()';
    };

    Blockly.JavaScript['if_then'] = function(block) {
      // get condition value (True or False)
      var value_condition
          = statementWithouHighlight(block, 'condition');

      // transform inner blocks to code
      var statements_condition_true
          = Blockly.JavaScript.statementToCode(block, 'condition_true');
      // construct Java Script if then statement
      var code = "if (" + value_condition + ") {" +
          statements_condition_true + "}";
      return code;
    };

    Blockly.JavaScript['if_then_else'] = function(block) {
      // get condition value (True or False)
      var value_condition
          = statementWithouHighlight(block, 'condition');

      // transform inner blocks to code (then branch)
      var statements_condition_true =
          Blockly.JavaScript.statementToCode(block, 'condition_true');
      // transform inner blocks to code (else branch)
      var statements_condition_false =
          Blockly.JavaScript.statementToCode(block, 'condition_false');
      // construct Java Script if then else statement
      var code = "if (" + value_condition + ") {" +
          statements_condition_true + "} else {" +
          statements_condition_false + "}";
      return code;
    };

    Blockly.JavaScript['for_loop_fixed'] = function(block) {
      // loop statements
      var statements =
          Blockly.JavaScript.statementToCode(block, 'body');

      var times = String(Number(block.getFieldValue('times')));
      var code = "for (var i = 0;" +
          "i<" + times + ";" +
          "i++){\n" +
          statements + "\n" +
          "}";
      return code;
    };

    Blockly.JavaScript['for_loop'] = function(block) {
      // loop statements
      var statements =
          Blockly.JavaScript.statementToCode(block, 'body');

      var from = String(Number(block.getFieldValue('from')));
      var to = String(Number(block.getFieldValue('to')));

      var loopVar = Blockly.JavaScript.variableDB_.getDistinctName(
                    'i', Blockly.Variables.NAME_TYPE);
      var code = "for (var " + loopVar +
          " = " + from + ";" +
          loopVar + "<=" + to + ";" +
          loopVar + "++){\n" +
          statements + "\n" +
          "}";
      return code;
    };


    Blockly.JavaScript['while_loop'] = function(block) {
      // loop statements
      var statements =
          Blockly.JavaScript.statementToCode(block, 'body');
      
      // get condition value (True or False)
      var value_condition
          = statementWithouHighlight(block, 'condition');

      var code = "while (" +
          value_condition +
          "){\n" +
          statements + "\n" +
          "}";
      return code;
    };

    /*
     * Redefinition of standard while/until loop
     */
    Blockly.JavaScript['controls_whileUntil'] = function(block) {
        // Do while/until loop.
        var until = block.getFieldValue('MODE') == 'UNTIL';
       
        // get condition value (True or False)
        var argument0
            = statementWithouHighlight(block, 'BOOL');

        var branch = Blockly.JavaScript.statementToCode(block, 'DO');
        branch = Blockly.JavaScript.addLoopTrap(branch, block.id);
        if (until) {
            argument0 = '!' + argument0;
        }
        return 'while (' + argument0 + ') {\n' + branch + '}\n';
    };

    /*
     * Redefinition of standard if/elseif/else block
     */
    Blockly.JavaScript['controls_if'] = function(block) {
        // If/elseif/else condition.
        var n = 0;
        var argument = statementWithouHighlight(block, 'IF' + n);

        var branch = Blockly.JavaScript.statementToCode(block, 'DO' + n);
        var code = 'if (' + argument + ') {\n' + branch + '}';
        
        for (n = 1; n <= block.elseifCount_; n++) {
            argument = statementWithouHighlight(block, 'IF' + n);
            branch = Blockly.JavaScript.statementToCode(block, 'DO' + n);
            code += ' else if (' + argument + ') {\n' + branch + '}';
            }
            if (block.elseCount_) {
                branch = Blockly.JavaScript.statementToCode(block, 'ELSE');
                code += ' else {\n' + branch + '}';
            }
        return code + '\n';
    };

    /**
     * Return generated JS code from statement but without any highlighting.
     * Especially useful when generating code as a condition.
     */
    function statementWithouHighlight(block, name) {
        // turn off prefixes for condition
        var oldPrefix = Blockly.JavaScript.STATEMENT_PREFIX;
        Blockly.JavaScript.STATEMENT_PREFIX = '';
        
        // get condition value (True or False)
        var statement
            = Blockly.JavaScript.statementToCode(block, name);

        // turn back on prefixes
        Blockly.JavaScript.STATEMENT_PREFIX = oldPrefix;
        
        return statement;
    }

    // TODO: code for Python...
  }

  // public API
  return {
    initializeBlockly: initializeBlockly
  };
}]);



