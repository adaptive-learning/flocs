/*
 * Controller for register page
 */
angular.module('flocs.user')
.controller('registerCtrl', ['$scope','$location','$log','$state','userDao', 
    function($scope,$location,$log, $state,userDao){
        
        $scope.model = {
            username : undefined,
            firstname : undefined,
            lastname : undefined,
            email : undefined,
			passwd : undefined,
            passwdCheck : undefined

        };
	    function register(){
            var username = $scope.model.username;
            var firstname = $scope.model.firstname;
            var lastname = $scope.model.lastname;
            var email = $scope.model.email;
			var passwd = $scope.model.password;
            var passwdCheck = $scope.model.vpassword;
            if (passwd === passwdCheck){
			    userDao.registerUser(username,firstname,lastname,email,passwd)
                    .then(function(response){
				        if(!response.data.errorMSG){
                            $state.go('home'); 
			            }else{
                            $scope.errorMSG = response.data.errorMSG; 
			            }
                    });
            }else{
                $scope.errorMSG = 'Hesla se neshodují';
            }
        }
        $scope.register = register;
}]);
