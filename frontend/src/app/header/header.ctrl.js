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

  // access to user info
  $scope.user = userService.user;

}]);
