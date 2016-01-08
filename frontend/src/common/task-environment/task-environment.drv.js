/*
 * Task Environment Directive
 */
angular.module('flocs.taskEnvironment')
.directive('flocsTaskEnvironment', function() {
  return {
    restrict: 'E',
    transclude: true,
    scope: {},
    templateUrl: 'task-environment/task-environment.tpl.html',
    controller: 'taskEnvironmentCtrl',
    link: function(scope, element, attrs) {
    }
  };
});
