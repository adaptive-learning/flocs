/**
 * Main practice controller
 * @ngInject
 */
angular.module('flocs.practice')
.controller('practiceCtrl', function ($scope, $timeout, ngDialog, $uibModal,
      $stateParams, practiceService, userService) {

  // TODO: move it to a template and unhardcode report values
  var template = '<div class=\"ngdialog-message\"> ' +
    ' <h3>Výborně, vyřešil si úlohu!</h3> ' +
    ' <h4>Jak těžká pro tebe byla?</h4> ' +
    '</div>' +
    '<div class="ngdialog-buttons">' +
    '<button type="button" style="background-color: orangered" class="ngdialog-button ngdialog-button-primary" ng-click="confirm(2)">Těžká</button>' +
    '<button type="button" style="background-color: #0040D0" class="ngdialog-button ngdialog-button-primary" ng-click="confirm(3)">Akorát</button>' +
    '<button type="button" style="background-color: #00A000" class="ngdialog-button ngdialog-button-primary" ng-click="confirm(4)">Lehká</button>' +
    '</div>';

  // report flow dialog options
  var dialogOptions = {
    template: template,
    plain: true,
    scope: $scope,
    showclose: false
  };

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
    practiceService.settingNextTask();
  }

  function taskRejected() {
    practiceService.settingNextTask();
  }

  function taskAttempted(attemptResult) {
    if (attemptResult.solved) {
      taskCompletionReporting().then(reportFilled, reportClosed);
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
    //var fillingPromise = ngDialog.openConfirm(dialogOptions);
    //return fillingPromise;
  }

  /**
   * Filling the report completes the task
   */
  function reportFilled(report) {
    practiceService.taskCompleted(report);
  }

  /**
   * If the report dialog is closed, continue with the current task
   */
  function reportClosed() {
    console.log('report closed');
    // continue practicing without sending final report
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
