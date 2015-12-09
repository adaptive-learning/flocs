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

    // first find whether user is already logged in (this is necessary e.g.
    // because of refresh, opening new tab etc.
    // Current behavior: if the user is not logged in, it just returns empty
    // username. TODO: make it more explicit, that the user is not logged in.
    userDao.loggedIn().then(function(response) {
      user.username = response.data.username;
      user.logged = (user.username) ? true : false;
    });

    // public API
	return {
      user: user,
      loggingIn: loggingIn,
      loggingOut: loggingOut
	};


}]);

