angular.module('flocs.directives')
.directive('flocsFlowMeter', function(flowFactory) {
  return {
    restrict: 'E',

    scope: {
      flow: '=',
      editable: '=',
      size: '@',
    },

    templateUrl: 'directives/flow-meter.tpl.html',

    controller: function($scope){
      $scope.flowValue = $scope.flow.getFlowValue();
      $scope.slider = {
        value: $scope.flowValue,
        options: {
          floor: -1,
          ceil: 1,
          step: 0.1,
          getPointerColor: flowFactory.valueToColor,
          showTicks: 1,
          hideLimitLabels: true,
          hidePointerLabels: true,
          readOnly: !($scope.editable),
        }
      };
      // need to force rerendering of the slider probably to show correctly in
      // the table (possible because the table adjust width of cells after the
      // initial rendering)
      $scope.$$postDigest(function () {$scope.$broadcast('rzSliderForceRender');});
    },

    link: function(scope, element, attrs) {
    }
  };
});
