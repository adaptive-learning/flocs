/*
 * Task Environment controller
 */
angular.module('flocs.taskEnvironment')
.controller('taskEnvironmentCtrl', ['$scope', 'taskService', 'mazeService',
  'workspaceService', 'interpreterService',
  function($scope, taskService, mazeService, workspaceService, interpreterService) {

  /*function nextTask() {
    //taskService.taskFinished().then(function() {
    taskService.gettingNextTask().then(function() {
      mazeService.set(taskService.getMazeSettings());
      workspaceService.set(taskService.getWorkspaceSettings());
    });
  }*/

  function run() {
    $scope.initialState = false;
    interpreterService.runCode().then(function(result) {
      if (result.solved) {
        console.log('Solved!');
      } else if (result.died) {
        console.log('Died!');
      }
    });
  }

  function reset() {
    interpreterService.stopExecution().then(function(result) {
      if (!result.solved) {
        mazeService.reset();
        $scope.initialState = true;
      }
    });
  }

  /*function runOrReset() {
    if ($scope.initialState) {
      $scope.initialState = false;
      run();
    } else if (!($scope.resetting)) {
      $scope.resetting = true;
      reset();
      $scope.initialState = true;
      $scope.resetting = false;
    }
  }*/

  // inital state
  $scope.initialState = true;
  $scope.noTask = true;
  //$scope.resetting = false;
  $scope.run = run;
  $scope.reset = reset;

  /*// set first task
  nextTask();*/

}]);
