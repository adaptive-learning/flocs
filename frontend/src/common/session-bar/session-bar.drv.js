/**
 * Session Bar Directive
 * @ngInject
 */
angular.module('flocs.sessionBar')
.directive('flocsSessionBar', function(practiceService) {
  return {
    restrict: 'E',
    scope: {},
    templateUrl: 'session-bar/session-bar.tpl.html',
    // @ngInject
    controller: function($scope) {
      $scope.session = practiceService.session;
    },
    link: function(scope, element, attrs) {
    }
  };
});
