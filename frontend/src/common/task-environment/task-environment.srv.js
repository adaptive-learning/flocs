/*
 * Task Environment Service
 */
angular.module('flocs.taskEnvironment')
.factory('taskEnvironmentService', ['taskDao', 'mazeService', 'workspaceService',
    function (taskDao, mazeService, workspaceService) {

  var currentTask = null;
  var afterAttemptCallback = null;

  // === public API ===
  return {
    settingNextTask: settingNextTask,
    settingTaskById: settingTaskById,
    setInitialState: setInitialState,
    attemptFinished: attemptFinished,

    //getMazeSettings: getMazeSettings,
    //getWorkspaceSettings: getWorkspaceSettings,
    //reportResults: reportResults,
    //taskFinished: taskFinished
  };

  // === private implementation ===

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

  function setTask(newTask) {
    currentTask = newTask;
    mazeService.set(getMazeSettings());
    workspaceService.set(getWorkspaceSettings());
  }

  function setInitialState() {
    mazeService.reset();
  }

  function settingTaskById(id) {
    taskDao.gettingTaskById(id)
      .then(function(newTask) {
        setTask(newTask);
      });
  }

  function settingNextTask(callback) {
    afterAttemptCallback = callback;
    var taskPromise = taskDao.gettingNextTask()
      .then(function(newTask) {
        setTask(newTask);
        return newTask;
      });
    return taskPromise;
  }

  function attemptFinished(result) {
    if (afterAttemptCallback) {
      afterAttemptCallback(result);
    }

    //$rootScope.$broadcast('task:attemptFinished');
    //console.log(result);
  }

}]);
