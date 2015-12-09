/*
 * Service for userManagement
 */
angular.module('flocs.services')
.factory('userDao',['$http', '$log', function($http, $log) {
	return {
        register: register,
        login : login,
        loggedIn : loggedIn,
        logout: logout
	};

	function register(username, email, passwd) {
      var data = {
          'username': username,
          'firstname': null, //firstname,
          'lastname': null, //lastname,
          'email': email,
          'password': passwd
      };
      return $http.post('api/user/register', data);
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

     function logout(){
     return $http.get('api/user/logout');
     }

}]);

