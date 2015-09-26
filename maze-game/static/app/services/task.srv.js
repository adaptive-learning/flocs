/*
 * Service for getting new tasks
 */
angular.module('flocs.services')
.factory('taskService', [function () {

  var currentTask;

  function getNextTask() {
    // TODO: unhardcode
    currentTask = {
      id: 0,
      mazeSettings: {
        grid: [
          [1, 1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1, 1],
          [1, 0, 0, 0, 0, 1, 1, 1],
          [1, 1, 1, 1, 0, 1, 1, 1],
          [1, 1, 1, 1, 0, 1, 1, 1],
          [1, 1, 1, 1, 0, 1, 1, 1],
          [1, 1, 1, 1, 0, 0, 2, 1],
          [1, 1, 1, 1, 1, 1, 1, 1]],
        hero: {
          position: [1, 2],
          direction: 0
        }
      },
      workspaceSettings: {
        toolbox: null,
      }
    };
    return currentTask;
  }

  function reportResults() {
    // TODO
  }

  // return public API
  return {
    getNextTask: getNextTask,
    reportResults: reportResults
  };
}]);
