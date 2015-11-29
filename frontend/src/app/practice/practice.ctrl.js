/*
 * Main practice controller
 */
angular.module('flocs.practice')
  .controller('practiceCtrl', ['$scope', '$timeout', 'ngDialog', 'practiceSessionService',
    function ($scope, $timeout, ngDialog, practiceSessionService) {

      // TODO move it to the template
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

      // start a new practice session
      practice();

      function practice() {
        // set task
        practiceSessionService.practicingTask().then(function () {
            // task resolved
            console.log('Task solved!');

            // ask for flow report
            var dialog = flowReportOpening();
            dialog.then(function (report) {
              practiceSessionService.sendFinalAttempt(report);

              // continue practicing
              practice();
            });
          }
        );
      }

      function flowReportOpening() {
        var dialog = ngDialog.openConfirm(dialogOptions);
        return dialog;
      }

    }]);

