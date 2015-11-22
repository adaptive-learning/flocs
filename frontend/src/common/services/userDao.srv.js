/*
 * Service for userManagement
 */
angular.module('flocs.services')
.factory('userDao',['$http', '$log', function($http, $log) {
	//
	return {
        registerUser: registerUser,
        login : login,
        loggedIn : loggedIn
	};

	function registerUser(username,firstname,lastname,email,passwd) {
		var data = {
			'username':username,
			'firstname':firstname,
			'lastname':lastname,
			'email':email,
			'password':passwd
		};
        $log.log(data);
		return $http.post ('api/user/register', data)
            .success(function(response){
		return response;
		});	
    }
	
     function login (username,passwd){
		var data = {
			'username':username,
			'password':passwd
		};
		return $http.post('api/user/login',data)
            .success(function(response){
		return response;
		});

	}

     function loggedIn(){
     return $http.get('api/user/loggedin');
     }

}]);

