/*
 * Access service
 */
angular.module('flocs.access')
.factory('accessService', function($q, userService) {

  var OK = 200;
  var UNAUTHORIZED = 401;
  var FORBIDDEN = 403;

  function isUserAvailable() {
    return userService.gettingUserDetails()
      .then(function success(user) {
        if (user.authenticated) {
          return OK;
        } else {
          return $q.reject(UNAUTHORIZED);
        }
      }, function error(user) {
          return $q.reject(UNAUTHORIZED);
      });
  }

  function isAuthenticated() {
    return userService.gettingUserDetails()
      .then(function success(user) {
        if (user.authenticated && !user.isLazyUser) {
          return OK;
        } else {
          return $q.reject(UNAUTHORIZED);
        }
      }, function error(user) {
          return $q.reject(UNAUTHORIZED);
      });
  }

  function isStaff() {
    return userService.gettingUserDetails()
      .then(function success(user) {
        if (user.authenticated && user.isStaff) {
          return OK;
        } else if (!user.authenticated || user.isLazyUser) {
          // maybe someone just forgot to log in
          return $q.reject(UNAUTHORIZED);
        } else {
          return $q.reject(FORBIDDEN);
        }
      }, function error(user) {
          return $q.reject(UNAUTHORIZED);
      });
  }

  return {
    OK: OK,
    UNAUTHORIZED: UNAUTHORIZED,
    FORBIDDEN: FORBIDDEN,
    isUserAvailable: isUserAvailable,
    isAuthenticated: isAuthenticated,
    isStaff: isStaff,
  };
});
