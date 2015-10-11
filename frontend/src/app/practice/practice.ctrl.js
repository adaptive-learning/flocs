/*
 * Main practice controller
 */
angular.module('flocs.practice')
.controller('practiceCtrl', ['$scope', 'taskService', 'mazeService',
  'workspaceService', 'interpreterService',
  function($scope, taskService, mazeService, workspaceService, interpreterService) {

  function nextTask() {
    //taskService.taskFinished().then(function() {
    taskService.gettingNextTask().then(function() {
      mazeService.set(taskService.getMazeSettings());
      workspaceService.set(taskService.getWorkspaceSettings());
    });
  }

  function run() {
    interpreterService.runCode().then(function(result) {
      if (result.solved) {
        // TODO: get new task from task service
        alert('Solved!');
      } else if (result.died) {
        alert('Died!');
      }
    });
  }

  function reset() {
    interpreterService.stopExecution().then(function(result) {
      if (!result.solved) {
        mazeService.reset();
      }
    });
  }

  function runOrReset() {
    if ($scope.initialState) {
      $scope.initialState = false;
      run();
    } else if (!($scope.resetting)) {
      $scope.resetting = true;
      reset();
      $scope.initialState = true;
      $scope.resetting = false;
    }
  }

  // inital state = program can be run
  $scope.initialState = true;
  $scope.resetting = false;
  $scope.runOrReset = runOrReset;

  // set first task
  nextTask();

}]);

