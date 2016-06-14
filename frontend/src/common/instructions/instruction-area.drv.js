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
      var instructionSeen = null;
      scope.visible = false;
      scope.active = false;

      scope.showing = function(instruction) {
        if (instructionSeen === null) {
          instructionSeen = $q.defer();
        }
        scope.text = instruction.text;
        scope.visible = true;
        scope.active = true;
        console.log('showing:', instruction);
        return instructionSeen.promise;
      };

      scope.close = function() {
        scope.visible = false;
        scope.active = false;
        if (instructionSeen !== null) {
          instructionSeen.resolve();
        }
      };

      instructionsService.registerInstructionArea(scope);
    }
  };
});
