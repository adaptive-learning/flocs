/*
 * Header controller
 */
angular.module('flocs.header')
.controller('headerCtrl', ['$scope', 'userService', '$uibModal', function($scope, userService, $uibModal) {

  $scope.openLoginModal = function() {
    var modalInstance = $uibModal.open({
        templateUrl: 'user/login-modal.tpl.html',
        controller: 'loginModalCtrl',
    });
  };

  $scope.logout = function() {
    userService.loggingOut();
  };

  // access to user info
  $scope.user = userService.user;

}]);
