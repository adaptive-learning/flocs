/*
 * Controller for task completion modal
 */
angular.module('flocs.user')
.controller('taskCompletionModalCtrl', function($scope, $uibModalInstance,
      $uibModal, practiceService, flowFactory) {

  $scope.reportFlow = function(flowKey) {
    // we try to convert the key to flow just to make sure the key corresponds
    // to an actual flow (to throw explicit error if the set of possible values
    // chagne)
    var flow = flowFactory.fromKey(flowKey);
    var report = {'flow': flow.key};
    $uibModalInstance.close(report);
  };

  $scope.evaluation = practiceService.attemptEvaluation;
  $scope.practiceInfo = practiceService.practiceInfo;
});

