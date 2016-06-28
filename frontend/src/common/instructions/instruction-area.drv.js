// @ngInject
angular.module('flocs.instructions')
.directive('flocsInstructionArea', function($q, $timeout, instructionsService) {

  function setPlacementWatcher(scope, placementParams) {

    function setPlacement(placement) {
      scope.placementCss.left = placement.left + 'px';
      scope.placementCss.top = placement.top + 'px';
      scope.placementCss.width = placement.width + 'px';
      scope.placementCss.height = placement.height + 'px';
    }

    var selector = placementParams.selector;
    var element = angular.element(document.querySelector(selector));
    var adjustPlacement = function(placement) {
      if (placementParams.getOffset) {
        var offset = placementParams.getOffset();
        placement.left += offset.x;
        placement.top += offset.y;
      }
      if (placementParams.getSize) {
        var size = placementParams.getSize();
        placement.width = size.width;
        placement.height = size.height;
      }
    };
    var getPlacement = null;
    if ('svg' in placementParams) {
      var svgSelector = selector + ' svg ' + placementParams.svg;
      var svgElement = angular.element(document.querySelector(svgSelector));
      getPlacement = function() {
        var parentPosition = element.position();
        var bbox = svgElement[0].getBBox();
        var placement = {
          left: parentPosition.left + bbox.x,
          top: parentPosition.top + bbox.y,
          width: bbox.width,
          height: bbox.height,
        };
        adjustPlacement(placement);
        return placement;
      };
    } else {
      getPlacement = function() {
        var position = element.position();
        var placement = {
          left: position.left,
          top: position.top,
          width: element.outerWidth(),
          height: element.outerHeight()
        };
        adjustPlacement(placement);
        return placement;
      };
    }
    scope.$watch(getPlacement, setPlacement, true);
  }

  return {
    restrict: 'E',
    scope: {
      key: '@',
      placement: '=',
      popoverPosition: '@',
    },
    templateUrl: 'instructions/instruction-area.tpl.html',
    link: function(scope, element, attrs) {
      var instructionSeen = null;
      scope.area = {
        visible: false
      };
      scope.placementCss = {
        left: '0',
        top: '0',
        width: '0',
        height: '0',
      };
      scope.instruction = {
        active: false,
        text: '',
        position: scope.popoverPosition || 'top',
      };

      scope.showing = function(instruction) {
        if (instructionSeen === null) {
          instructionSeen = $q.defer();
        }
        scope.instruction.text = instruction.text;
        scope.instruction.active = true;
        $timeout(function() {
          scope.area.visible = true;
        });
        setPlacementWatcher(scope, scope.placement);
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
