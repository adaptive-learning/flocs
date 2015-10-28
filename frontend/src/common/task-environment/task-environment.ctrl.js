/*
 * Task Environment controller
 */
angular.module('flocs.taskEnvironment')
.controller('taskEnvironmentCtrl', ['$scope', 'taskEnvironmentService', 'interpreterService',
  function($scope, taskEnvironmentService, interpreterService) {

  function run() {
    $scope.initialState = false;
    interpreterService.runCode().then(function(result) {
      taskEnvironmentService.attemptFinished(result);
    });
  }

  function reset() {
    interpreterService.stopExecution().then(function(result) {
      //if (!result.solved) {...}
      taskEnvironmentService.setInitialState();
      $scope.initialState = true;
    });
  }

  /*function handleTaskEnvironmentChange() {
    $scope.blocksStatus.used = taskEnvironmentService.getBlocksUsed();
    $scope.blocksStatus.limit = taskEnvironmentService.getBlocksLimit();
  }*/

  $scope.initialState = true;
  $scope.blocksStatus = taskEnvironmentService.blocksStatus;
  $scope.run = run;
  $scope.reset = reset;

}]);
