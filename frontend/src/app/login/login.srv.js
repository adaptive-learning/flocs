/*
 * User service
 */
angular.module('flocs.user')
.factory('userService', ['$q', 'userDao', function($q, userDao) {
    var user = {
      logged: false,
      username: undefined
    };

    function loggingIn(username, password) {
      return userDao.login(username, password).then(function(response) {
        if (response.data.loggedIn == 1) {
          // successfully logged in
          user.logged = true;
          user.username = username;
        } else {
          return $q.reject('authentication failed');
        }
      });
    }

    function loggingOut() {
      return userDao.logout().then(function(){
        user.logged = false;
      });
    }

    // first find wheter user is already logged in (this is necessary e.g.
    // because of refresh, opening new tab etc.
    userDao.loggedIn().then(function(response) {
      user.logged = true;
      user.username = response.data.username;
    });

    // public API
	return {
      user: user,
      loggingIn: loggingIn,
      loggingOut: loggingOut
	};


}]);

