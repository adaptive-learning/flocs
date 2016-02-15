/*
 * Controller for task completion modal
 */
angular.module('flocs.user')
.controller('taskCompletionModalCtrl', function($scope, $uibModalInstance,
      $uibModal, practiceService) {

  $scope.reportFlow = function(flowValue) {
    var report = {'flow': flowValue};
    $uibModalInstance.close(report);
  };

  $scope.evaluation = practiceService.attemptEvaluation;

});

