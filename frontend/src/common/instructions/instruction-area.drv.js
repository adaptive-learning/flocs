// @ngInject
angular.module('flocs.instructions')
.directive('flocsInstructionArea', function($q, instructionsService) {
  return {
    restrict: 'E',
    transclude: true,
    scope: {
      key: '@',
    },
    templateUrl: 'instructions/instruction-area.tpl.html',
    link: function(scope, element, attrs) {
      scope.active = false;
      scope.visible = false;

      scope.showing = function(instruction) {
        var instructionSeen = $q.defer();
        scope.text = instruction.text;
        scope.visible = true;
        scope.active = true;
        console.log('showing:', instruction);
        return instructionSeen.promise;
      };

      instructionsService.registerInstructionArea(scope);
    }
  };
});
