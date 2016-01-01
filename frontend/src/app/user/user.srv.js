/*
 * User service
 */
angular.module('flocs.user')
.factory('userService', function($q, $state, $uibModal, userDao) {
    var user = {
      logged: false,
      username: undefined
    };
    var deferredUser = $q.defer();

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

    function checkingIfLoggedIn() {
      return deferredUser.promise.then(function() {
        return user.logged;
      });
    }

    function ensuringLoggedIn() {
      return checkingIfLoggedIn().then(function(isLogged) {
        if (isLogged) {
          return;
        }
        // if not logged, open login modal
        var loginModal = $uibModal.open({
            templateUrl: 'user/login-modal.tpl.html',
            controller: 'loginModalCtrl',
        });
        return loginModal.result;
      });
    }

    function loggingOut() {
      return userDao.logout().then(function(){
        user.logged = false;
        $state.go('home', {});
      });
    }

    // first find whether user is already logged in (this is necessary e.g.
    // because of refresh, opening new tab etc.
    // Current behavior: if the user is not logged in, it just returns empty
    // username. TODO: make it more explicit, that the user is not logged in.
    userDao.loggedIn().then(function(response) {
      user.username = response.data.username;
      user.logged = (user.username) ? true : false;
      deferredUser.resolve();
    }, function() {
      deferredUser.resolve();
    });

    // public API
	return {
      user: user,
      loggingIn: loggingIn,
      loggingOut: loggingOut,
      ensuringLoggedIn: ensuringLoggedIn
	};

});
