/**
 * Footer controller
 *
 * @ngInject
 */
angular.module('flocs.footer')
.controller('footerCtrl', function($scope, $uibModal, localesService) {

  $scope.currentLanguageCode = localesService.getLanguage();
  $scope.languageDomains = localesService.getLanguageDomains();

  $scope.openFeedbackModal = function() {
    var modalInstance = $uibModal.open({
        templateUrl: 'feedback/feedback-modal.tpl.html',
        controller: 'feedbackModalCtrl',
    });
  };

});
