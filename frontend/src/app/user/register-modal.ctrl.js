/*
 * Controller for register page
 */
angular.module('flocs.user')
.controller('registerModalCtrl', function($scope, $uibModalInstance, $log,
      $state, userService) {

  $scope.registrationData = {
    username: '',
    email: '',
    password: '',
    vpassword: ''
  };

  function register() {
    var username = $scope.registrationData.username;
    var email = $scope.registrationData.email;
    var password = $scope.registrationData.password;

    if (password === $scope.registrationData.vpassword) {
      userService.signingUp(username, email, password)
        .then(function success(response) {
          // TODO: show message: registration successful?
          $uibModalInstance.close();
          $state.go($state.current, {}, {reload: true});
        }, function error(response) {
          var httpStatus = response.status;
          if (httpStatus == 400) {
            $scope.errorMessage = 'REGISTER_MODAL.USERNAME_TAKEN';
          } else {
            $scope.errorMessage = 'REGISTER_MODAL.OTHER_ERROR';
          }
        });
    } else {
      $scope.errorMessage = 'REGISTER_MODAL.PASSWORDS_DIFFER';
    }
  }

  function close() {
    $uibModalInstance.dismiss();
  }

  $scope.register = register;
  $scope.close = close;
});
