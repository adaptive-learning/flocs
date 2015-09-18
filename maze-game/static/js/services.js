/* Services */
angular.module('flocs.services', [])

/*
 * Enum type for types of boxes (squares) in a maze
 */
.constant('BoxType', {
  FREE: 0,
  WALL: 1,
  START: 2,
  GOAL:  3
})

/*
 * Factory service for getting new tasks
 */
.factory('taskFactory', [function () {

  var currentTask;

  function getNewTask() {
    // TODO: unhardcode
    currentTask = {
      'id': 0,
      'grid': [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 3, 1],
        [1, 1, 1, 1, 1, 1, 1, 1]],
      'direction': 0
    };
    return currentTask;
  }

  function reportResults() {
    // TODO
  }

  // return public API
  return {
    getNewTask: getNewTask,
    reportResults: reportResults
  };
}])

/*
 * Factory service exposing Blockly workspace API
 */
.factory('workspaceFactory', [function () {

  // local variables (private attributes)
  var _workspace;

  function setWorkspace(workspace) {
    _workspace = workspace;
  }

  function setToolbox(toolbox) {
    // TODO
  }

  function highlightBlock(id) {
    _workspace.highlightBlock(id)
  }

  function getJavaScriptCode() {
    // TODO: add optional highlight
    //Blockly.JavaScript.STATEMENT_PREFIX = 'highlightBlock(%1);\n';
    //Blockly.JavaScript.addReservedWords('highlightBlock');
    var code = Blockly.JavaScript.workspaceToCode(_workspace);
    return code;
  }

  function getPythonCode() {
    var code = Blockly.Python.workspaceToCode(_workspace);
    return code
  };

  // return public API
  return {
    setWorkspace: setWorkspace,
    setToolbox: setToolbox,
    getJavaScriptCode: getJavaScriptCode,
    getPythonCode: getPythonCode,
    highlightBlock: highlightBlock
  };
}])

/*
 * Factory service exposing maze API
 */
.factory('mazeFactory', ['$rootScope', 'directionService', 'BoxType',
  function($rootScope, directionService, BoxType) {

  // private attributes
  var grid, initialDirection, direction, initalPosition, position;

  /*
      Register new view to listen for visualization events
  */
  function registerView(reset, move, turn) {
    $rootScope.$on('maze:reset', function(event, args) {
      reset(grid, initialPosition, initialDirection);
    });
    $rootScope.$on('maze:move', function(event, args) {
      move(position);
    });
    $rootScope.$on('maze:turn', function(event, args) {
      turn(direction);
    });

    // initialize the new view
    reset(grid, position, direction);
  }

  /*
      Find position of the start square
  */
  function findInitialPosition(grid) {
    for (var i = 0; i < grid.length; i++) {
      for (var j = 0; j < grid[i].length; j++) {
        if (grid[i][j] == BoxType.START) {
          return [j, i];
        }
      }
    }
  }

  function setNewTask(taskDescription) {
    grid = taskDescription.grid;
    initialPosition = findInitialPosition(grid);
    initialDirection = taskDescription.direction;
    resetTask();
  }

  function resetTask() {
    position = angular.copy(initialPosition);
    direction = angular.copy(initialDirection);
    $rootScope.$broadcast('maze:reset');
  }

  /*
   * Move the hero 1 step in the current direction
   */
  function moveForward() {
    var movement = directionService.directionVector(direction);
    position[0] += movement[0];
    position[1] += movement[1];
    $rootScope.$broadcast('maze:move');
  }

  /*
   * Turn the hero by 90 degrees
   * @param turnDirection: 1 = turn left, -1 = turn right
   */
  function turn(turnDirection) {
    // NOTE: JavaScript modulo is not positive for positive inputs so we add 4
    // before taking modulo to make sure it's positive
    direction = (direction + turnDirection + 4) % 4;
    $rootScope.$broadcast('maze:turn');
  }

  /*
   * Return true if the hero reached the goal
   */
  function solved() {
    var solved = (grid[position[1]][position[0]] == BoxType.GOAL);
    return solved;
  }

  /*
   * Return true if the hero died
   */
  function died() {
    var died = (grid[position[1]][position[0]] == BoxType.WALL);
    return died;
  }

  // return public API
  return {
    registerView: registerView,
    setNewTask: setNewTask,
    resetTask: resetTask,
    moveForward: moveForward,
    turn: turn,
    solved: solved,
    died: died
  };
}])

/*
 * Factory for interpreting code
 */
.factory('interpreterFactory', ['mazeFactory', 'workspaceFactory',
         function (mazeFactory, workspaceFactory) {

  function initApi(interpreter, scope) {
    // highlighting blocks
    interpreter.setProperty(scope, 'highlightBlock',
      interpreter.createNativeFunction(function(id) {
        id = id ? id.toString() : '';
        return interpreter.createPrimitive(workspaceFactory.highlightBlock(id));
    }));

    // moveForward() blocks
    interpreter.setProperty(scope, 'moveForward',
      interpreter.createNativeFunction(function() {
        return interpreter.createPrimitive(mazeFactory.moveForward());
    }));

    // turnLeft() blocks
    interpreter.setProperty(scope, 'turnLeft',
      interpreter.createNativeFunction(function() {
        return interpreter.createPrimitive(mazeFactory.turn(1));
    }));

    // turnRight() blocks
    interpreter.setProperty(scope, 'turnRight',
      interpreter.createNativeFunction(function() {
        return interpreter.createPrimitive(mazeFactory.turn(-1));
    }));

  }

  function runCode() {
    var code = workspaceFactory.getJavaScriptCode();
    // initialize interpreter
    // TODO je nutne inicializovat api interpreteru pro kazdy kod znova??
    var interpreter = new Interpreter(code, initApi);
    // TODO krokovat pomaleji + highlight
    var result = {
      solved: false,
      died: false
    };
    var ok = true;
    while (ok && !result.solved && !result.died) {
      ok = interpreter.step();
      // TODO: pauzy (jen pri highlightu, interpret dela vic kroku)
      if (mazeFactory.died()) {
        result.died = true;
      } else if (mazeFactory.solved()) {
        result.solved = true;
      }
    }
    return result;
  }

  // return public API
  return {
    runCode: runCode
  };

}])

/*
 * Direction service
 */
.service('directionService', function() {
  this.directionVector = function(direction) {
    switch (direction) {
      case 0: return [1, 0];
      case 1: return [0, -1];
      case 2: return [-1, 0];
      case 3: return [0, 1];
    }
  };
});
