/*
 * Task Environment controller
 */
angular.module('flocs.taskEnvironment')
.controller('taskEnvironmentCtrl', ['$scope', 'taskEnvironmentService', 'interpreterService',
  function($scope, taskEnvironmentService, interpreterService) {

  /*function nextTask() {
    taskEnvironmentService.settingNextTask(); // <- move to practice ctrl
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
      //if (!result.solved) {...}
      taskEnvironmentService.setInitialState();
      $scope.initialState = true;
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
  //$scope.noTask = true;
  //$scope.resetting = false;
  $scope.run = run;
  $scope.reset = reset;

  /*// set first task
  nextTask();*/

}]);
