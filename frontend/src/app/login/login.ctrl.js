/*
 * Controller for login form
 */
angular.module('flocs.user')
.controller('loginCtrl',['$scope', '$log', '$state', '$uibModalInstance', '$uibModal', 'userService',
	function($scope, $log, $state, $uibModalInstance, $uibModal, userService){

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
                $uibModalInstance.dismiss('login-successful');
                $state.go($state.current, {}, {reload: true});
              }, function() {
                //$log.log(response.data.msg);
                $scope.errormsg = "Zadali jste špatné údaje!";
              });
      }

      function register() {
        $uibModalInstance.dismiss('clicked-register');
        var modalInstance = $uibModal.open({
            templateUrl: 'login/register-modal.tpl.html',
            controller: 'registerCtrl',  //'registerModalCtrl',
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
}]);

