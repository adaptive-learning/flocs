/*
 * Header controller
 */
angular.module('flocs.header')
.controller('headerCtrl', function($scope, userService, $uibModal, practiceService, $state) {

  $scope.openLoginModal = function() {
    var modalInstance = $uibModal.open({
        templateUrl: 'user/login-modal.tpl.html',
        controller: 'loginModalCtrl',
    });
  };

  $scope.logout = function() {
    userService.loggingOut();
  };

  $scope.navCollapsed = true;
  $scope.user = userService.user;
  $scope.session = practiceService.session;
  $scope.practiceInfo = practiceService.practiceInfo;
  $scope.$state = $state;

});
