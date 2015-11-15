/*
 * Controller for login form
 */
angular.module('flocs.user', [])
.factory('UserDao',['$http', function($http) {
	//
	return {
	};

	function registerUser(username,firstname,lastname,email,passwd) {
		var data = {
			'username':username,
			'firstname':firstname,
			'lastname':lastname,
			'email':email,
			'password':passwd
		};
		return $http.post({
				url: 'api/user/register',
			        data: data,
		});
	}
	
	function login(username,passwd){
		var data = {
			'username':username,
			'password':passwd
		};
		return $http.post({
				url:'api/user/login',
				data: data
		});
	}

}])
.controller('loginCtrl',['$scope','UserDao',
	function($scope,UserDao){
		var username = $scope['username'];
		var passwd = $scope['passwd'];
		return UserDao.login(username, passwd);
}]);

