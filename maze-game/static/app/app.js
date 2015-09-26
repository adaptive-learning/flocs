/**
 * Flocs application modul
 */
angular.module('flocs', [
    'ngRoute',
    'flocs.services',
    'flocs.practice',
])

// routes configuration
.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/practice', {
        templateUrl: '/static/app/practice/practice.tpl.html',
        controller: 'practiceCtrl'
      }).
      otherwise({
        redirectTo: '/practice'
      });
}])

// Main application controller
.controller('appCtrl', ['$scope', function($scope) {
  // global configuration (user, language) functions go here
}]);
