// @ngInject
angular.module('flocs.instructions')
.directive('flocsInstructionArea', function($q, instructionsService) {
  return {
    restrict: 'E',
    transclude: true,
    scope: {
      key: '@',
      popoverPosition: '@',
    },
    templateUrl: 'instructions/instruction-area.tpl.html',
    link: function(scope, element, attrs) {
      var instructionSeen = null;
      scope.area = {
        visible: false
      };
      scope.instruction = {
        active: false,
        text: '',
        position: 'top', //scope.popoverPosition,
      };

      scope.showing = function(instruction) {
        if (instructionSeen === null) {
          instructionSeen = $q.defer();
        }
        scope.instruction.text = instruction.text;
        scope.instruction.position = scope.popoverPosition || 'top';
        scope.instruction.active = true;
        scope.area.visible = true;
        console.log('showing:', instruction);
        return instructionSeen.promise;
      };

      scope.close = function() {
        scope.area.visible = false;
        scope.instruction.active = false;
        if (instructionSeen !== null) {
          instructionSeen.resolve();
        }
      };

      instructionsService.registerInstructionArea(scope);
    }
  };
});
