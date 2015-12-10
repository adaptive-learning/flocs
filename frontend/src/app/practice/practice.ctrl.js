/*
 * Main practice controller
 */
angular.module('flocs.practice')
  .controller('practiceCtrl', ['$scope', '$timeout', 'ngDialog', '$uibModal', 'practiceSessionService', 'userService',
    function ($scope, $timeout, ngDialog, $uibModal, practiceSessionService, userService) {

      // TODO move it to a template
      var template = '<div class=\"ngdialog-message\"> ' +
        ' <h3>Výborně, vyřešil si úlohu !</h3> ' +
        ' <h4>Jak těžká pro tebe byla?</h4> ' +
        '</div>' +
        '<div class="ngdialog-buttons">' +
        '<button type="button" style="background-color: orangered" class="ngdialog-button ngdialog-button-primary" ng-click="confirm(1)">Těžká</button>' +
        '<button type="button" style="background-color: #0040D0" class="ngdialog-button ngdialog-button-primary" ng-click="confirm(2)">Akorát</button>' +
        '<button type="button" style="background-color: #00A000" class="ngdialog-button ngdialog-button-primary" ng-click="confirm(3)">Lehká</button>' +
        '</div>';

      // report flow dialog options
      var dialogOptions = {
        template: template,
        plain: true,
        scope: $scope,
        showclose: false
      };

      /**
       * Filling the report completes the task
       */
      function reportFilled(report) {
        practiceSessionService.taskCompleted(report);
      }

      /**
       * If the report dialog is closed, continue with the current task
       */
      function reportClosed() {
        console.log('report closed');
        // continue practicing without sending final report
      }

      /**
       * Open a report dialog and return a promise of filling the report
       */
      function flowReportFilling() {
        var fillingPromise = ngDialog.openConfirm(dialogOptions);
        return fillingPromise;
      }

      function taskFinished() {
        practiceNextTask();
      }

      // TODO: implement "giving up a task" ("Give me easier task")
      function taskRejected() {
        throw "Function taskRejected() not implemented yet.";
      }

      function taskAttempted(attemptResult) {
        if (attemptResult.solved) {
            flowReportFilling().then(reportFilled, reportClosed);
        }
      }

      /**
       * Practice new task
       */
      function practiceNextTask() {
        practiceSessionService.practicingTask().then(
            taskFinished,
            taskRejected,
            taskAttempted);
      }

      // NOTE: quick a dirty solution to make usert to log in; TODO: use lazy
      // user at backend, do not force to log in immediately
      // start a new practice session
      userService.ensuringLoggedIn().then(practiceNextTask);
}]);
