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
        "id": "maze_if_then",
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
        "id": "maze_if_then_else",
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
      }
    ];
    // load all blocks
    for (var i = 0, jsonBlock; jsonBlock = blocksList[i]; i++) {
      Blockly.Blocks[jsonBlock.id] = {
        init: (function(data) {return function() {this.jsonInit(data);};})(jsonBlock)
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

    Blockly.JavaScript['maze_if_then'] = function(block) {
      // turn off prefixex for condition
      var oldPrefix = Blockly.JavaScript.STATEMENT_PREFIX;
      Blockly.JavaScript.STATEMENT_PREFIX = '';
      
      // get condition value (True or False)
      var value_condition
          = Blockly.JavaScript.statementToCode(block, 'condition');
      
      // turn back on prefixes
      Blockly.JavaScript.STATEMENT_PREFIX = oldPrefix;

      // transform inner blocks to code
      var statements_condition_true 
          = Blockly.JavaScript.statementToCode(block, 'condition_true');
      // construct Java Script if then statement
      var code = "if (" + value_condition + ") {"
          + statements_condition_true + "}";
      return code;
    };

    Blockly.JavaScript['maze_if_then_else'] = function(block) {
      // turn off prefixex for condition
      var oldPrefix = Blockly.JavaScript.STATEMENT_PREFIX;
      Blockly.JavaScript.STATEMENT_PREFIX = '';

      // get condition value (True or False)
      var value_condition
          = Blockly.JavaScript.statementToCode(block, 'condition');

      // turn back on prefixes
      Blockly.JavaScript.STATEMENT_PREFIX = oldPrefix;

      // transform inner blocks to code (then branch)
      var statements_condition_true =
          Blockly.JavaScript.statementToCode(block, 'condition_true');
      // transform inner blocks to code (else branch)
      var statements_condition_false =
          Blockly.JavaScript.statementToCode(block, 'condition_false');
      // construct Java Script if then else statement
      var code = "if (" + value_condition + ") {"
          + statements_condition_true + "} else {"
          + statements_condition_false + "}";
      return code;
    };
    // TODO: code for Python...
  }

  // public API
  return {
    initializeBlockly: initializeBlockly
  };
}]);



