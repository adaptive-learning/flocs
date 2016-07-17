/*
 * Controller for sign up page
 */
angular.module('flocs.user')
.controller('signUpModalCtrl', function($scope, $uibModalInstance, $log,
      $state, userService, $window) {

  $scope.personalDetails = {
    username: '',
    email: '',
    password: '',
    vpassword: undefined
  };

  function signUp() {
    if ($scope.personalDetails.password === $scope.personalDetails.vpassword) {
      userService.signingUp($scope.personalDetails.username,
                            $scope.personalDetails.email,
                            $scope.personalDetails.password)
        .then(function success(response) {
          // TODO: show message: registration successful?
          $uibModalInstance.close();
          $state.go($state.current, {}, {reload: true});
        }, function error(response) {
          var httpStatus = response.status;
          if (httpStatus == 400) {
            $scope.errorMessage = 'SIGN_UP_MODAL.USERNAME_TAKEN';
          } else {
            $scope.errorMessage = 'SIGN_UP_MODAL.OTHER_ERROR';
          }
        });
    } else {
      $scope.errorMessage = 'SIGN_UP_MODAL.PASSWORDS_DIFFER';
    }
  }

  function close() {
    $uibModalInstance.dismiss();
  }

  function socialLogin(backend) {
    $window.location = '/social/login/' + backend + '/';
  }


  $scope.signUp = signUp;
  $scope.socialLogin = socialLogin;
  $scope.close = close;
});
