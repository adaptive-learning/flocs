/**
 * Main practice controller
 * @ngInject
 */
angular.module('flocs.practice')
.controller('practiceCtrl', function ($scope, $timeout, $state, ngDialog, $uibModal,
      $stateParams, practiceService, userService) {

  function practiceTask(taskId) {
    $scope.taskPrepared = false;
    $scope.taskLoading = true;
    practiceService.settingTaskById(taskId).then(function() {
      $scope.taskPrepared = true;
      $scope.taskLoading = false;
      practiceService.practicingTask().then(
        taskFinished,
        taskRejected,
        taskAttempted);
    });
  }

  function taskFinished(result) {
    if (practiceService.isSessionOver()) {
      $state.go('session-overview');
    } else {
      practiceService.settingNextTask();
    }
  }

  function taskRejected() {
    if (practiceService.isSessionOver()) {
      $state.go('session-overview');
    } else {
       practiceService.settingNextTask();
    }
  }

  function taskAttempted(attemptResult) {
    if (attemptResult.solved) {
      taskCompletionReporting().then(reportFilled);
    }
  }

  /**
   * Open a report dialog and return a promise of filling the report
   */
  function taskCompletionReporting() {
    var modalInstance = $uibModal.open({
      templateUrl: 'practice/task-completion-modal.tpl.html',
      controller: 'taskCompletionModalCtrl',
    });
    return modalInstance.result;
  }

  function reportFilled(report) {
    // filling the report completes the task
    practiceService.taskCompleted(report);
  }

  function giveUp() {
    practiceService.giveUpTask();
  }

  $scope.taskPrepared = false;
  $scope.taskLoading = false;
  $scope.giveUp = giveUp;

  var taskId = $stateParams.taskId;
  practiceTask(taskId);
});
