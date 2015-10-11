/*
 * Service for getting new tasks
 */
angular.module('flocs.services.task', [])
.factory('taskService', ['$http', function ($http) {

  // public API
  return {
    gettingNextTask: gettingNextTask,
    //reportResults: reportResults,
    getMazeSettings: getMazeSettings,
    getWorkspaceSettings: getWorkspaceSettings,
    //taskFinished: taskFinished
  };

  // private implementation

  var currentTask;

  function getMazeSettings() {
    return currentTask['maze-settings'];
  }

  function getWorkspaceSettings() {
    return currentTask['workspace-settings'];
  }

  function gettingNextTask() {

    // TODO: error handling etc., separate service
    return $http.get('api/practice/next-task')
      .then(function(response) {
        currentTask = response.data;
      });


    /*currentTask = {
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
      return currentTask;*/
  }

  function reportResults() {
    // TODO
  }
}]);
