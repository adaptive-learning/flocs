/*
 * Module for all flocs directives.
 */
angular.module('flocs.directives', [
])

.directive('switchDomain', function($rootScope, $location) {

  function appendCurrentPath(domain) {
    return domain + $location.path();
  }

  return {
    restrict: 'A',
    scope: {
      domain: "@switchDomain"
    },
    link: function(scope, element, attrs) {
      attrs.$set('href', appendCurrentPath(scope.domain));
      $rootScope.$on("$stateChangeSuccess", function() {
        attrs.$set('href', appendCurrentPath(scope.domain));
      });
    }
  };
});
