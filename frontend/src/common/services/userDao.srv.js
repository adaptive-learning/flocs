/**
 * Service for userManagement
 * @ngInject
 */
angular.module('flocs.services')
.factory('userDao', function($http, $log) {
	return {
        signingUp: signingUp,
        loggingIn : loggingIn,
        loggingOut: loggingOut,
        gettingUserDetails: gettingUserDetails,
	};

	function signingUp(username, email, password) {
      var data = {
          'username': username,
          'firstname': null, //firstname,
          'lastname': null, //lastname,
          'email': email,
          'password': password
      };
      // succes and failure differentiated by HTTP codes
      return $http.post('/api/user/signup', data);
    }

     function loggingIn (username,password){
		var data = {
			'username':username,
			'password':password
		};
        // succes and failure differentiated by HTTP codes
		return $http.post('/api/user/login',data);
	}

    function loggingOut(){
      return $http.post('/api/user/logout');
    }

    function gettingUserDetails() {
      return $http.get('/api/user/details').then(parseUserDetails);
    }

    function parseUserDetails(response) {
      var user = {
        username: response.data['username'],
        firstName: response.data['first-name'],
        lastName: response.data['last-name'],
        authenticated: response.data['authenticated'],
        isLazyUser: response.data['is-lazy-user'],
        email: response.data['email'],
        isStaff: response.data['is-staff'],
        providers: response.data['providers'],
      };
      return user;
    }
});
