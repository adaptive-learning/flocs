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

  function handleTaskEnvironmentChange() {
    //$scope.blocksUsed = taskEnvironmentService.getBlocksUsed();
    //$scope.blocksLimit = taskEnvironmentService.getBlocksLimit();

    $scope.blocksStatus.used = taskEnvironmentService.getBlocksUsed();
    $scope.blocksStatus.limit = taskEnvironmentService.getBlocksLimit();
  }

  function hack() {
  }

  $scope.initialState = true;
  $scope.blocksStatus = {
    used: null,
    limit: null
  };
  $scope.run = run;
  $scope.reset = reset;

  taskEnvironmentService.addChangeListener(handleTaskEnvironmentChange);
  // TODO remove listener on destroy...??
  //handleTaskEnvironmentChange();


}]);
