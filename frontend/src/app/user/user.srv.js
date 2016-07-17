/*
 * User service
 */
angular.module('flocs.user')
.factory('userService', function($rootScope, $state, userDao) {

    var user = {
        username: "",
        firstName: "",
        lastName: "",
        authenticated: false,
        isLazyUser: false,
        email: "",
        isStaff: false,
        providers: [],
      };

    var emptyUser = {
        username: "",
        firstName: "",
        lastName: "",
        authenticated: false,
        isLazyUser: false,
        email: "",
        isStaff: false,
        providers: [],
      };

    function onUserChange(callback) {
      $rootScope.$on("flocs:user:change", callback);
    }

    function loggingIn(username, password) {
      return userDao.loggingIn(username, password)
        .then(function success() {
          gettingUserDetails();
          $rootScope.$emit("flocs:user:change");
        });
    }
    
    function loggingOut() {
      return userDao.loggingOut().then(function(){
        setUserToEmpty();
        $state.go('logout', {});
        $rootScope.$emit("flocs:user:change");
      });
    }

    function signingUp(username, email, password) {
      return userDao.signingUp(username, email, password)
        .then(function success() {
          gettingUserDetails();
          // TODO: if the registration is not succesful, the promise
          // should be rejected not solved with data.errorMSG!!
          $rootScope.$emit("flocs:user:change");
        });
    }

    function gettingUserDetails() {
      return userDao.gettingUserDetails()
        .then(function success(newUser) {
          copyUser(newUser);
          return user;
        }, function error() {
          setUserToEmpty();
          return user;
        });
    }

    function isUserAvailable() {
      return user.authenticated;
    }

    function setUserToEmpty() {
      copyUser(emptyUser);
    }

    function copyUser(newUser) {
      for (var prop in newUser) {
        user[prop] = newUser[prop];
      }
    }

    // run when loaded
    gettingUserDetails()
      .then(function() {
        if (user.authenticated && !user.isLazyUser) {
          $rootScope.$emit("flocs:user:change");
        }
    });
    
        
    // public API
	return {
      user: user,
      isUserAvailable: isUserAvailable,
      loggingIn: loggingIn,
      loggingOut: loggingOut,
      signingUp: signingUp,
      gettingUserDetails: gettingUserDetails,
      onUserChange: onUserChange,
	};
});
