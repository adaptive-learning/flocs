/*
 * Module for all flocs directives.
 */
angular.module('flocs.directives', [
  'rzModule',  // for slider
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
})

.directive('flocsAbsolutePlacement', function() {
  return {
    restrict: 'A',
    scope: {
      placement: '=',
    },
    link: function(scope, element, attrs) {
      scope.placementStyle = {
        position: 'absolute',
        display: 'inline-block',
        left: scope.placement.left,
        top: scope.placement.top,
        width: scope.placement.width,
        height: scope.placement.height,
      };
    },
  };
})

.directive('flocsProxyElement', function($timeout) {

  function findElement(selector) {
    var element = angular.element(document.querySelector(selector))[0];
    return element || null;
  }

  return {
    restrict: 'E',
    scope: {
      selector: '@',
    },
    template: '<span ng-style="proxyStyle"/>',
    link: function(scope, element, attrs) {
      scope.proxyStyle = {
        position: 'relative',
        display: 'inline-block',
        left: 0,
        top: 0,
        width: 0,
        height: 0,
      };

      // The source element might not exist yet (e.g. for Blockly SVG, it may
      // take several hundreds-thousands of milliseconds). In such case, timer
      // is set up repeatedly until until the source element appears.
      var sourceElement = findElement(scope.selector);
      function askForElementUntilFound(interval) {
        $timeout(function() {
          sourceElement = findElement(scope.selector);
          if (sourceElement === null) {
            askForElementUntilFound(interval*2);
          }
        }, interval);
      }
      askForElementUntilFound(400);

      scope.placement = null;
      function getPlacement() {
        if (!sourceElement) {
          return null;
        } else {
          var bbox = sourceElement.getBBox();
          return {
            left: bbox.x,
            top: bbox.y,
            width: bbox.width,
            height: bbox.height,
          };
        }
      }

      // TODO: avoid watcher
      scope.$watch(getPlacement, function(newPlacement) {
        if (newPlacement !== null) {
          console.log('new placement:', newPlacement);
          scope.proxyStyle.left = Math.floor(newPlacement.left) + 'px';
          scope.proxyStyle.top = Math.floor(newPlacement.top) + 'px';
          scope.proxyStyle.width = Math.floor(newPlacement.width) + 'px';
          scope.proxyStyle.height = Math.floor(newPlacement.height) + 'px';
        }
      }, true);

    }
  };
});
