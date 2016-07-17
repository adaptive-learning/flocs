/*
 * Controller for login form
 */
angular.module('flocs.user')
.controller('loginModalNoTransitionsCtrl', function($scope, $log, $uibModalInstance,
      $uibModal, userService, $window){

  $scope.credentials = {
      username: undefined,
      password: undefined
  };
  $scope.errorMessage = "";

  function login() {
    userService.loggingIn($scope.credentials.username,
                          $scope.credentials.password)
      .then(function success() {
        $uibModalInstance.close();
      }, function error() {
        // no other possibility thank to frontend checks in modal it self
        $scope.errorMessage = "LOGIN_MODAL.INCORRECT_USERNAME_OR_PASSWORD";
      });
  }

  function signUp() {
    var modalInstance = $uibModal.open({
        templateUrl: 'user/sign-up-modal.tpl.html',
        controller: 'signUpModalCtrl',
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

  function socialLogin(backend) {
    $window.location = '/social/login/' + backend + '/';
  }

  $scope.login = login;
  $scope.socialLogin = socialLogin;
  $scope.signUp = signUp;
  $scope.close = close;
});
