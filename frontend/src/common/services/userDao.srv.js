/**
 * Service for userManagement
 * @ngInject
 */
angular.module('flocs.services')
.factory('userDao', function($http, $log) {
	return {
        signingUp: signingUp,
        login : login,
        loggedIn : loggedIn,
        logout: logout,
        gettingUserDetails: gettingUserDetails,
	};

	function signingUp(username, email, passwd) {
      var data = {
          'username': username,
          'firstname': null, //firstname,
          'lastname': null, //lastname,
          'email': email,
          'password': passwd
      };
      return $http.post('/api/user/register', data);
    }

     function login (username,passwd){
		var data = {
			'username':username,
			'password':passwd
		};
		return $http.post('/api/user/login',data)
            .success(function(response){
		  return response;
		});
	}

    function loggedIn(){
      return $http.get('/api/user/loggedin');
    }

    function logout(){
      // TODO: logout should not be GET!
      return $http.get('/api/user/logout');
    }

    function gettingUserDetails() {
      return $http.get('/api/user/details')
        .then(function(response) {
          return response.data;
        });
    }
});
