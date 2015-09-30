/**
 * Maze component modul
 */
angular.module('flocs.maze', [])

/**
 * Enum type for types of boxes (squares) in a maze
 */
.constant('BoxType', {
  FREE: 0,
  WALL: 1,
  GOAL: 2
});
