/*
 * Controller for login form
 */
angular.module('flocs.user')
.controller('loginModalCtrl', function($scope, $log, $state, $uibModalInstance,
      $uibModal, userService){

  $scope.loginForm = {};
  // TODO: rename model (meaning: info *from modal* about user)
  $scope.model = {
      username: undefined,
      password: undefined
  };

  function login() {
      var username = $scope.model.username;
      var passwd = $scope.model.password;
      userService.loggingIn(username, passwd)
        .then(function() {
            $scope.errormsg = "";
            $uibModalInstance.close('login-successful');
            $state.go($state.current, {}, {reload: true});
          }, function() {
            //$log.log(response.data.msg);
            $scope.errormsg = "Zadali jste špatné údaje!";
          });
  }

  function register() {
    var modalInstance = $uibModal.open({
        templateUrl: 'user/register-modal.tpl.html',
        controller: 'registerModalCtrl',
    });
    $uibModalInstance.close();
    modalInstance.result.then(function(result) {
      /*
      NOTE: logging after successful signing up was moved to the server
      // and log the user in
      userService.loggingIn(result.username, result.password).then(function() {
        $uibModalInstance.close();
      });
      */
    });
  }

  function logout(){
      userService.loggingOut().then(function(response){
          $state.go($state.current, {}, {reload: true});
      });
  }

  $scope.login = login;
  $scope.register = register;
  $scope.logout = logout;
});

