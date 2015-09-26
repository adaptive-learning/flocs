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
    // TODO: code for Python...
  }

  // public API
  return {
    initializeBlockly: initializeBlockly
  };
}]);



