/*
 * Service for userManagement
 */
angular.module('flocs.services')
.factory('UserDao',['$http', function($http) {
	//
	return {
        registerUser: registerUser,
        login : login
	};

	function registerUser(username,firstname,lastname,email,passwd) {
		var data = {
			'username':username,
			'firstname':firstname,
			'lastname':lastname,
			'email':email,
			'password':passwd
		};
		return $http({
            method: 'POST',
			url:'api/user/register',
			data: data,
            headers: {'Content-Type': 'application/x-www-form-urlencoded'}
		}).then(function(response){
		return response;
		});	
    }
	
     function login (username,passwd){
		var data = {
			'username':username,
			'password':passwd
		};
		return $http({
            method: 'POST',
			url:'api/user/login',
			data: data,
            headers: {'Content-Type': 'application/x-www-form-urlencoded'}
		}).then(function(response){
		return response;
		});

	}

}]);

