/*
 * Controller for login form
 */
angular.module('flocs.user',[])
.controller('loginCtrl',['$scope','$location','UserDao',
	function($scope,$location,UserDao){
		function send(){
			var username = $scope['username'];
			var passwd = $scope['passwd'];
			if (UserDao.login(username, passwd) == 1){
				$location.url(".");
			}else{
				$location.url("/403.html");
			}

		}
    $scope.send = send;
}]);

