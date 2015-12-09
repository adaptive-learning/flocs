/*
 * Controller for register page
 */
angular.module('flocs.user')
.controller('registerCtrl', ['$scope','$uibModalInstance','$log','$state','userDao',
    function($scope, $uibModalInstance, $log, $state,userDao){
	    function register(){
          var username = $scope['username'];
          //$log.log($scope['username']);
          //var firstname = $scope['firstname'];
          //var lastname = $scope['lastname'];
          var email = $scope['email'];
          var password = $scope['password'];
          var passwdCheck = $scope.model.vpassword;
          if (password === passwdCheck){
            userDao.register(username, email, password)
              .then(function(response) {
                // TODO: if the registration is not succesful, the promise
                // should be rejectet not solved with data.errorMSG!!
				if(!response.data.errorMSG){
                  // TODO: show message: registration successful
                  $uibModalInstance.dismiss('registration-successful');
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
