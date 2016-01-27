/**
 * Footer controller
 *
 * @ngInject
 */
angular.module('flocs.footer')
.controller('footerCtrl', function($scope, $uibModal) {

  $scope.openFeedbackModal = function() {
    var modalInstance = $uibModal.open({
        templateUrl: 'feedback/feedback-modal.tpl.html',
        controller: 'feedbackModalCtrl',
    });
  };

});
