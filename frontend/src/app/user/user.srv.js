/*
 * User service
 */
angular.module('flocs.user')
.factory('userService', function($rootScope, $q, $state, $uibModal, $timeout, userDao) {
    var user = {
      logged: false,
      lazyLogged: false,
      username: undefined,
      email: undefined,
    };
    var deferredUser = $q.defer();

    function onUserChange(callback) {
      $rootScope.$on("flocs:user:change", callback);
    }

    function loggingIn(username, password) {
      return userDao.login(username, password).then(function(response) {
        if (response.data.loggedIn == 1) {
          // successfully logged in
          user.logged = true;
          user.username = username;
          $rootScope.$emit("flocs:user:change");
          if ($state.is('logout-success')) {
            $timeout(function() {$state.go('home');});
          }
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
        user.lazyLogged = false;
        $state.go('logout-success', {});
        $rootScope.$emit("flocs:user:change");
      });
    }

    function signingUp(username, email, password) {
      return userDao.signingUp(username, email, password)
        .then(function(response) {
          // TODO: if the registration is not succesful, the promise
          // should be rejected not solved with data.errorMSG!!
          if(!response.data.errorMSG){
            user.logged = true;
            user.lazyLogged = false;
            user.username = username;
            $rootScope.$emit("flocs:user:change");
          }
          return response;
        });
    }

    function gettingUserDetails() {
      return userDao.gettingUserDetails().then(function(details) {
        user.username = details.username;
        user.email = details.email;
        return user;
      });
    }

    // first find whether user is already logged in (this is necessary e.g.
    // because of refresh, opening new tab etc.
    // Current behavior: if the user is not logged in, it just returns empty
    // username. TODO: make it more explicit, that the user is not logged in.
    userDao.loggedIn().then(function(response) {
      user.username = response.data.username;
      user.logged = Boolean(user.username) && !response.data['is-lazy-user'];
      user.lazyLogged = response.data['is-lazy-user'];
      if (isUserAvailable()) {
        $rootScope.$emit("flocs:user:change");
      }
      deferredUser.resolve();
    }, function() {
      deferredUser.resolve();
    });

    function isUserAvailable() {
      return user.logged || user.lazyLogged;
    }

    function setUserAvailable() {
      if (!user.logged && !user.lazyLogged) {
        user.lazyLogged = true;
        $rootScope.$emit("flocs:user:change");
      }
    }

    function waitUntilLogged() {
      var userLogged = $q.defer();
      checkingIfLoggedIn().then(function(logged) {
        if (logged) {
          userLogged.resolve();
        } else {
          userLogged.notify('NOT_LOGGED_YET');
        }
      });
      return userLogged.promise;
    }

    // public API
	return {
      user: user,
      setUserAvailable: setUserAvailable,
      isUserAvailable: isUserAvailable,
      ensuringLoggedIn: ensuringLoggedIn,
      loggingIn: loggingIn,
      loggingOut: loggingOut,
      signingUp: signingUp,
      gettingUserDetails: gettingUserDetails,
      onUserChange: onUserChange,
      waitUntilLogged: waitUntilLogged,
	};

});
