/*
 * Task Environment Service
 */
angular.module('flocs.taskEnvironment')
.factory('taskEnvironmentService', function (taskDao, mazeService,
      workspaceService, interpreterService) {

  var currentTask = null;
  var afterAttemptCallback = null;
  //var changeListeners = [];
  var blocksStatus = {
    used: null,
    limit: null
  };
  var toolsStatus = {
    picked: null,
    all: null
  };
  var executionStatus = {
    initialState: true
  };
  var instructions = {
      text: null
  };

  workspaceService.addChangeListener(handleWorkspaceChange);
  mazeService.addChangeListener(handleMazeChange);

  // === public API ===
  return {
    setTask:         setTask,
    settingTaskById: settingTaskById,
    settingTaskByIdWithToolbox: settingTaskByIdWithToolbox,
    //setInitialState: setInitialState,
    //attemptFinished: attemptFinished,

    runningCode: runningCode,
    stoppingExecution: stoppingExecution,


    // NOTE: we have used shared data (blocksStatus instead of listeners)
    //addChangeListener: addChangeListener,
    //getBlocksUsed: getBlocksUsed,
    //getBlocksLimit: getBlocksLimit,

    // shared data
    blocksStatus: blocksStatus,
    toolsStatus: toolsStatus,
    executionStatus: executionStatus,
    instructions: instructions,
    getCurrentTask: getCurrentTask,

    //getMazeSettings: getMazeSettings,
    //getWorkspaceSettings: getWorkspaceSettings,
    //reportResults: reportResults,
    //taskFinished: taskFinished
  };

  // === private implementation ===

  /**
   * Add new listener which will be called when the environment changes.
   */
  /*function addChangeListener(listener) {
    changeListeners.push(listener);

    // if a task has been already set, call the listener to get initital state
    if (currentTask !== null) {
      listener();
    }
  }*/

  /**
   * Call all change listeners
   */
  /*function changeNotification() {
    angular.forEach(changeListeners, function(listener) {
      listener();
    });
  }*/

  function getMazeSettings() {
    if (currentTask === null) {
      return null;
    }
    return currentTask['maze-settings'];
  }

  function getWorkspaceSettings() {
    if (currentTask === null) {
      return null;
    }
    return currentTask['workspace-settings'];
  }

  function getBlocksUsed() {
    return workspaceService.getBlocksUsed();
  }

  function getBlocksLimit() {
    return workspaceService.getBlocksLimit();
  }

  function getTokensPicked() {
    return mazeService.getTokensPicked();
  }

  function getTokensAll() {
    return mazeService.getTokensAll();
  }

  /*
   * Set a new task in the environment. Optionally specify a callback to call
   * after each attempt of the user.
   */
  function setTask(newTask, _afterAttemptCallback, instructionsText) {
    afterAttemptCallback = _afterAttemptCallback || null;
    instructionsText = instructionsText || [];
    currentTask = newTask;
    mazeService.set(getMazeSettings());
    workspaceService.set(getWorkspaceSettings());
    executionStatus.initialState = true;
    //changeNotification();
    instructions.text = instructionsText.join(' ');
  }

  function setInitialState() {
    mazeService.reset();
    executionStatus.initialState = true;
  }

  function settingTaskById(id) {
    taskDao.gettingTaskById(id)
      .then(function(newTask) {
        setTask(newTask);
      });
  }
  
  function settingTaskByIdWithToolbox(id) {
    taskDao.gettingTaskByIdWithToolbox(id)
      .then(function(newTask) {
        setTask(newTask);
      });
  }


  function attemptFinished(result) {
    if (afterAttemptCallback) {
      afterAttemptCallback(result);
    }

    //$rootScope.$broadcast('task:attemptFinished');
    //console.log(result);
  }

  function runningCode() {
    executionStatus.initialState = false;
    var promise = interpreterService.runCode().then(function(result) {
      attemptFinished(result);
    });
    return promise;
  }

  function stoppingExecution() {
    var promise = interpreterService.stopExecution().then(function(result) {
      setInitialState();
    });
    return promise;
  }

  function handleWorkspaceChange() {
    //changeNotification();
    blocksStatus.used = getBlocksUsed();
    blocksStatus.limit = getBlocksLimit();
  }

  function handleMazeChange() {
    toolsStatus.picked = getTokensPicked();
    toolsStatus.all = getTokensAll();
  }

  function getCurrentTask() {
    return currentTask;
  }

});
