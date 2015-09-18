/* Directives */
angular.module('flocs.directives', [])

.directive('flocsWorkspace', ['workspaceFactory', function(workspaceFactory) {
  return {
    restrict: 'E',
    scope: {},
    templateUrl: '/static/partials/workspace.html',

    /*controller: function($scope) {

      $scope.getJavaScriptCode = function() {
        var code = Blockly.JavaScript.workspaceToCode(scope.workspace);
        return code
      };

    },*/

    link: function(scope, element) {

      // initialize blockly
      var blocksList = [// TODO: move to a service
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

      var workspace = Blockly.inject('blocklyDiv',
        {toolbox: document.getElementById('toolbox')}); // TODO: unhard-code toolbox
      workspaceFactory.setWorkspace(workspace);
    }
  };
}])

.directive('flocsMaze', ['BoxType', 'mazeFactory', function(BoxType, mazeFactory) {
  return {
    restrict: 'E',
    scope: {},
    templateUrl: '/static/partials/maze.html',
    /*controller: function($scope){
    },*/
    link: function(scope, element){

      // image paths
      var getBoxImagePath = function(box) {
        switch (box) {
          case BoxType.WALL: return '/static/img/box.svg';
          case BoxType.GOAL: return '/static/img/goal.png';
          default: return null;
        }
      };

      /*
         Reset the maze.
      */
      function reset(grid, initialPosition, initialDirection){
        var gridSize = grid.length;
        var visualization = {
          width: 300,
          height: 300
        };
        visualization.boxSize = visualization.width / gridSize,
        scope.hero = {
          x: initialPosition[0],
          y: initialPosition[1],
          direction: initialDirection,
          width: visualization.boxSize,
          height: visualization.boxSize,
          path: '/static/img/karlik2.png'
        }
        visualization.boxes = [];
        for (var i = 0; i < gridSize; i++) {
          for (var j = 0; j < gridSize; j++) {
            visualization.boxes.push({
              x: j, // * visualization.boxSize,
              y: i, // * visualization.boxSize,
              width: visualization.boxSize,
              height: visualization.boxSize,
              path: getBoxImagePath(grid[i][j])
            });
          }
        }
        visualization.boxes.push(scope.hero);
        // publish new visualization
        scope.visualization = visualization;
      };

      function move(position) {
        // TODO: animation
        //var vector = directionService.directionVector(scope.hero.direction);
        scope.hero.x = position[0];
        scope.hero.y = position[1];
      };

      function turn(newDirection) {
        // TODO: animation
        scope.hero.direction = newDirection;
      };

      // interface of the maze component (via event signals)
      mazeFactory.registerView(reset, move, turn);

    }
  };
}])
