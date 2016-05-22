/*
 * Module for all flocs directives.
 */
angular.module('flocs.directives', [
])

.directive('flocsTimeMeter', function() {
  return {
    restrict: 'E',
    scope: {
      'time': '@',
      'percentil': '@',
    },
    template: '<span class="timeMeter" ng-style="percentilStyle" title="percentil {{percentil}} %">{{time | secondsToTime}}</span>',
    link: function(scope, element, attrs) {
      // the higher percentil, the more dark yellow color
      // (shades of yellow are determined by the amount of blue)
      var blue = Math.round(220 - 2.1 * scope.percentil);
      scope.percentilStyle = {
        'background-color': 'rgb(250, 250, ' + blue + ')',
      };
    }
  };
})

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
