/*
 * Maze Filters
 */
angular.module('flocs.maze')

.filter('pixelCoordinates', function () {
  return function(input, visualization) {
    return input * visualization.boxSize;
  };
});
