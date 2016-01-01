/**
 * Direction Service
 * @ngInject
 */
angular.module('flocs.maze')
.service('gridService', function(BoxType) {
  /**
   * Convert direction ID to direction vector.
   */
  this.directionVector = function(direction) {
    switch (direction) {
      case 0: return [1, 0];
      case 1: return [0, -1];
      case 2: return [-1, 0];
      case 3: return [0, 1];
    }
  };

  /**
   * Return type of box on given position
   */
  this.boxAt = function(grid, position) {
    return grid[position[1]][position[0]];
  };

});
