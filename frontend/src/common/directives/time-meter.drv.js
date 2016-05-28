angular.module('flocs.directives')
.directive('flocsTimeMeter', function() {

  function percentilToColor(percentil) {
      // the higher percentil, the more dark yellow color
      // (shades of yellow are determined by the amount of blue)
      var blue = Math.round(220 - 2.1 * percentil);
      var color = 'rgb(250, 250, ' + blue + ')';
      return color;
  }

  return {
    restrict: 'E',
    scope: {
      'time': '@',
      'percentil': '@',
    },
    templateUrl: 'directives/time-meter.tpl.html',
    controller: function($scope){
      $scope.slider = {
        value: $scope.percentil,
        options: {
          floor: 0,
          ceil: 100,
          getPointerColor: percentilToColor,
          hideLimitLabels: true,
          hidePointerLabels: true,
          readOnly: true,
        }
      };
    },
    link: function(scope, element, attrs) {
    }
  };
});
