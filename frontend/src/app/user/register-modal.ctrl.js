/*
 * Controller for register page
 */
angular.module('flocs.user')
.controller('registerModalCtrl', ['$scope','$uibModalInstance','$log','$state','userDao', 'userService',
    function($scope, $uibModalInstance, $log, $state, userDao, userService) {
        $scope.registrationData = {
          username: '',
          email: '',
          password: '',
          vpassword: ''
        };

	    function register() {
          var username = $scope.registrationData.username;
          //$log.log($scope['username']);
          //var firstname = $scope['firstname'];
          //var lastname = $scope['lastname'];
          var email = $scope.registrationData.email;
          var password = $scope.registrationData.password;
          var passwdCheck = $scope.registrationData.vpassword;
          if (password === passwdCheck){
            userDao.register(username, email, password)
              .then(function(response) {
                // TODO: if the registration is not succesful, the promise
                // should be rejectet not solved with data.errorMSG!!
				if(!response.data.errorMSG){
                  // TODO: show message: registration successful
                  $uibModalInstance.close({username: username, password: password});
                } else {
                  $scope.errorMSG = response.data.errorMSG;
                }
              }, function(errorMessage) {
                // TODO: implement registration rejection
                $scope.errorMSG = errorMessage;
              });
          } else {
            $scope.errorMSG = 'Hesla se neshodují';
          }

          //} else {
          //  $state.go($state.current, {}, {reload: true});
          //}
        }
        $scope.register = register;
}]);
