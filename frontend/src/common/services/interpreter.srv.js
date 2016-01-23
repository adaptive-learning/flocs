/**
 * Service for code interpreting.
 * @ngInject
 */
angular.module('flocs.services')
.factory('interpreterService', function ($log, $timeout, mazeService, workspaceService) {

  var executing = false;
  var runCodePromise = null;
  var highlightPause = false;

  // speed settings
  var MIN_PAUSE = 0;
  var MAX_PAUSE = 400;
  var MIN_SPEED_LEVEL = 1;
  var MAX_SPEED_LEVEL = 3;
  var speed = 2;

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

    // turn
    var wrapper = function(direction) {
        return interpreter.createPrimitive(mazeService.turn(direction));
    };
    interpreter.setProperty(scope, 'turn',
      interpreter.createNativeFunction(wrapper));

    // checkBomb()
    interpreter.setProperty(scope, 'checkBomb',
      interpreter.createNativeFunction(function() {
        return interpreter.createPrimitive(
                mazeService.checkBox(
                    mazeService.getBoxType('GOAL')));
    }));

    // checkColour()
    wrapper = function(color) {
        return interpreter.createPrimitive(
                mazeService.checkBox(
                    mazeService.getBoxType(color)));
    };

    interpreter.setProperty(scope, 'checkColor',
        interpreter.createNativeFunction(wrapper));

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
    // checkPathFront()
    interpreter.setProperty(scope, 'checkPathFront',
      interpreter.createNativeFunction(function() {
        return interpreter.createPrimitive(mazeService.checkPath(0));
    }));
    // checkPath()
    wrapper = function(direction) {
        return interpreter.createPrimitive(mazeService.checkPath(direction));
    };
    interpreter.setProperty(scope, 'checkPath',
      interpreter.createNativeFunction(wrapper));
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
    var result = {
      solved: false,
      died: false
    };
    var ok = true;
    // code generation is safe and checked in workspaceService
    var code = workspaceService.getJavaScriptCode();

    try {
      var interpreter = new Interpreter(code, initApi);
    } catch (err) {
      // TODO: proper exception handling
      $log.warn("There has been a syntax error in user code.");
      $log.warn(err);
      runCodePromise = $timeout(function () {return result;}, 0); 
      return runCodePromise;
    }

    var stepCode = function () {
      // check executing flag (= request to stop execution)
      if (!executing) {
        return result;
      }

      try {
        // do one step of execution
        ok = interpreter.step();
      } catch (err) {
        // TODO: properly handle execption
        $log.warn("User code caused exception while interpreting.");   
        $log.warn(err);   
        executing = false;
        return result;
      }

      // check the maze status
      if (mazeService.died()) {
        result.died = true;
      } else if (mazeService.solved()) {
        result.solved = true;
      }

      // check whether to continue
      if (ok && executing && !result.died && !result.solved) {
        var pauseLength = 0;
        if (highlightPause)  {
          pauseLength = getPauseLength();
          highlightPause = false;
        }
        return $timeout(stepCode, pauseLength);
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

  /**
   * Return list of available speed levels
   */
  function getAvailableSpeeds() {
    var levels = [];
    for (var level = MIN_SPEED_LEVEL; level <= MAX_SPEED_LEVEL; level++){
      levels.push(level);
    }
    return levels;
  }

  /**
   * Return current speed level
   */
  function getSpeed() {
    return speed;
  }

  /**
   * Set new speed level
   */
  function setSpeed(newSpeed) {
    speed = newSpeed;
  }

  /**
   * Calculate length of pause in milliseconds from current speed level
   */
  function getPauseLength() {
    var slope = (MIN_PAUSE - MAX_PAUSE) / (MAX_SPEED_LEVEL - MIN_SPEED_LEVEL);
    var pause = MAX_PAUSE + slope * (speed - MIN_SPEED_LEVEL);
    return pause;
  }

  // return public API
  return {
    runCode: runCode,
    stopExecution: stopExecution,
    getAvailableSpeeds: getAvailableSpeeds,
    getSpeed: getSpeed,
    setSpeed: setSpeed
  };

});
