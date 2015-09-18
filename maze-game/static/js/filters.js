/* Filters */
angular.module('flocs.filters', [])

.filter('pixelCoordinates', function () {
  return function(input, visualization) {
    return input * visualization.boxSize;
  };
});
