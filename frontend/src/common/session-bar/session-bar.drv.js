/**
 * Session Bar Directive
 * @ngInject
 */
angular.module('flocs.sessionBar')
.directive('flocsSessionBar', function(sessionBarService) {
  return {
    restrict: 'E',
    scope: {},
    templateUrl: 'session-bar/session-bar.tpl.html',
    // @ngInject
    controller: function($scope) {
      $scope.sessionTasksStatuses = sessionBarService.sessionTasksStatuses;
    },
    link: function(scope, element, attrs) {
    }
  };
});
