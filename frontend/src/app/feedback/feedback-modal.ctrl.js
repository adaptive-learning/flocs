/**
 * Controller for feedback modal
 */
angular.module('flocs.feedback')
.controller('feedbackModalCtrl', function($scope, $uibModalInstance, feedbackDao) {

  $scope.feedback = {
    text: "",
    email: "",
  };

  $scope.status = {
    processed: false,
    success: false
  };

  $scope.sendFeedback = function() {
    feedbackDao.sendingFeedback($scope.feedback).then(function(response) {
      $scope.status.processed = true;
      $scope.status.success = response.success;
    });
  };

  $scope.close = function() {
    $uibModalInstance.dismiss('cancel');
  };

});

