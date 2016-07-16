/*
 * Controller for login form
 */
angular.module('flocs.user')
.controller('loginModalNoTransitionsCtrl', function($scope, $log, $uibModalInstance,
      $uibModal, userService){

  $scope.loginForm = {};
  $scope.credentials = {
      username: undefined,
      password: undefined
  };
  $scope.errorMessage = "";

  function login() {
    var username = $scope.model.username;
    var password = $scope.model.password;
    userService.loggingIn(username, password)
      .then(function success() {
        $uibModalInstance.close();
      }, function error() {
        // no other possibility thank to frontend checks in modal it self
        $scope.errorMessage = "LOGIN_MODAL.INCORRECT_USERNAME_OR_PASSWORD";
      });
  }

  function register() {
    var modalInstance = $uibModal.open({
        templateUrl: 'user/register-modal.tpl.html',
        controller: 'registerModalCtrl',
    });
    modalInstance.result.then(function success() {
        // NOTE: logging after successful signing up was moved to the server
        $uibModalInstance.close();
      }, function dismiss() {
        $uibModalInstance.dismiss();
      });
  }

  function close() {
    $uibModalInstance.dismiss();
  }

  $scope.login = login;
  $scope.register = register;
  $scope.close = close;
});
