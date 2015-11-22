/*
 * Controller for register page
 */
angular.module('flocs.user')
.controller('registerCtrl', ['$scope','$location','$log','userDao', 
    function($scope,$location,$log,userDao){

	    function send(){
            var username = $scope['username'];
            $log.log($scope['username']);
            var firstname = $scope['firstname'];
            var lastname = $scope['lastname'];
            var email = $scope['email'];
			var passwd = $scope['password'];
			if (userDao.registerUser(username,firstname,lastname,email,passwd) === true){
				$location.url("/succes.html");
			}else{
				$location.url("/");
			}
        }
        $scope.send = send;
}]);
