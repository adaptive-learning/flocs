/*
 * Controller for register page
 */
angular.module('flocs.user')
.controller('registerCtrl', ['$scope','$location','$log','$state','userDao', 
    function($scope,$location,$log, $state,userDao){
	    function register(){
            var username = $scope['username'];
            $log.log($scope['username']);
            var firstname = $scope['firstname'];
            var lastname = $scope['lastname'];
            var email = $scope['email'];
			var passwd = $scope['password'];
			if (userDao.registerUser(username,firstname,lastname,email,passwd) === true){
				$state.go('home'); 
			}else{
				$state.go($state.current, {}, {reload: true}); 
			}
        }
        $scope.register = register;
}]);
