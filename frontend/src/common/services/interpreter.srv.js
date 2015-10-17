/*
 * Service for code interpreting.
 */
angular.module('flocs.services')
.factory('interpreterService', ['$log', '$timeout', 'mazeService', 'workspaceService',
function ($log, $timeout, mazeService, workspaceService) {

  var executing = false;
  var runCodePromise = null;
  var highlightPause = false;

  /**
   * Define commands semantics.
   */
  function initApi(interpreter, scope) {
    // blocks highlighting
    interpreter.setProperty(scope, 'highlightBlock',
      interpreter.createNativeFunction(function(id) {
        id = id ? id.toString() : '';
        return interpreter.createPrimitive(function() {
            workspaceService.highlightBlock(id);
            highlightPause = true;}());
    }));

    // moveForward()
    interpreter.setProperty(scope, 'moveForward',
      interpreter.createNativeFunction(function() {
        return interpreter.createPrimitive(mazeService.moveForward());
    }));

    // turnLeft()
    interpreter.setProperty(scope, 'turnLeft',
      interpreter.createNativeFunction(function() {
        return interpreter.createPrimitive(mazeService.turn(1));
    }));

    // turnRight()
    interpreter.setProperty(scope, 'turnRight',
      interpreter.createNativeFunction(function() {
        return interpreter.createPrimitive(mazeService.turn(-1));
    }));
    // checkPathLeft()
    interpreter.setProperty(scope, 'checkPathLeft',
      interpreter.createNativeFunction(function() {
        return interpreter.createPrimitive(mazeService.checkPath(1));
    }));
    // checkPathRight()
    interpreter.setProperty(scope, 'checkPathRight',
      interpreter.createNativeFunction(function() {
        return interpreter.createPrimitive(mazeService.checkPath(-1));
    }));

  }

  /**
   * Execute code step by step.
   */
  function runCode() {
    // check if not already executing
    if (executing) {
      $log.warn('Already executing code. Ignoring another request to runCode.');
      return;
    }
    executing = true;
    var code = workspaceService.getJavaScriptCode();
    var interpreter = new Interpreter(code, initApi);
    var result = {
      solved: false,
      died: false
    };
    var ok = true;

    var stepCode = function () {
      // check executing flag (= request to stop execution)
      if (!executing) {
        return result;
      }

      // do one step of execution
      ok = interpreter.step();

      // check the maze status
      if (mazeService.died()) {
        result.died = true;
      } else if (mazeService.solved()) {
        result.solved = true;
      }

      // check whether to continue
      if (ok && executing && !result.died && !result.solved) {
        var pauseTime = 0;
        if (highlightPause)  {
          // TODO: unhardcode the pause time
          pauseTime = 500;
          highlightPause = false;
        }
        return $timeout(stepCode, pauseTime);
      } else {
        executing = false;
        return result;
      }
    };
    runCodePromise = $timeout(stepCode, 0);
    return runCodePromise;
  }

  /**
   * Set flag to stop execution.
   */
  function stopExecution() {
    executing = false;
    return runCodePromise;
  }

  // return public API
  return {
    runCode: runCode,
    stopExecution: stopExecution
  };

}]);
