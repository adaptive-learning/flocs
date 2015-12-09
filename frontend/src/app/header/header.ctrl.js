/*
 * Header controller
 */
angular.module('flocs.header')
.controller('headerCtrl', ['$scope', 'userService', '$uibModal', function($scope, userService, $uibModal) {

  $scope.openLoginModal = function() {
    var modalInstance = $uibModal.open({
        templateUrl: 'login/login-modal.tpl.html',
        controller: 'loginCtrl',  //'loginModalCtrl',
    });
  };

  $scope.logout = function() {
    userService.loggingOut();
  };

  // access to user info
  $scope.user = userService.user;

}]);
