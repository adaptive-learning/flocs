/*
 * Task Environment controller
 */
angular.module('flocs.taskEnvironment')
.controller('taskEnvironmentCtrl', function($scope, taskEnvironmentService, interpreterService, instructionsService) {

  function run() {
    //$scope.initialState = false;
    taskEnvironmentService.runningCode();
    /*.then(function(result) {
      if (result.solved) {
        $scope.initialState = true;
      }
    });*/
  }

  function reset() {
    taskEnvironmentService.stoppingExecution();
    /*.then(function(result) {
      $scope.initialState = true;
    });*/
  }

  /*function handleTaskEnvironmentChange() {
    $scope.blocksStatus.used = taskEnvironmentService.getBlocksUsed();
    $scope.blocksStatus.limit = taskEnvironmentService.getBlocksLimit();
  }*/

  $scope.changeSpeedClicked = function() {
    interpreterService.setSpeed($scope.settings.speed);
  };

  $scope.availableSpeeds = interpreterService.getAvailableSpeeds();
  $scope.settings = {
    speed: interpreterService.getSpeed()
  };

  $scope.executionStatus = taskEnvironmentService.executionStatus;
  $scope.blocksStatus = taskEnvironmentService.blocksStatus;
  $scope.toolsStatus = taskEnvironmentService.toolsStatus;
  $scope.getCurrentTask = taskEnvironmentService.getCurrentTask;
  $scope.run = run;
  $scope.reset = reset;
  $scope.blockInstructionsPlacements = instructionsService.blockInstructionsPlacements;

});
