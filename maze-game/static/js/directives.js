/* Directives */
angular.module('maze-game.directives', [])

.directive('flocsMaze', ['mazeApiService', function(mazeApi) {
  return {
    restrict: 'E',
    scope: {},
    templateUrl: '/static/partials/maze.html',
    controller: function($scope){

      // move one step forward [TODO: in given direction]
      function forward(){
        $scope.position[0] += 1;
      };

      /*
         Run the program. Return true/false whether the goal was reached.
      */
      function run(){
        //console.log(mazeApi.code);
        // TODO: vykonavani prikazu - pomoci $timeoutu a pozdeji i s mezistavy
        // (ulozit do nejake fronty), staci asi pozice
        $scope.position[0] = 7;
        // rekneme, ze to bylo uspesne:
        mazeApi.broadcastSuccess();
      };

      /*
         Reset the maze.
      */
      function reset(){
        hero = {
          x: initialPosition[1],
          y: initialPosition[0],
          width: visualization.boxSize,
          height: visualization.boxSize,
          path: '/static/img/karlik2.png'
        }
        visualization.boxes = [];
        for (var i = 0; i < gridSize; i++) {
          for (var j = 0; j < gridSize; j++) {
            visualization.boxes.push({
              x: j, // * visualization.boxSize,
              y: i, // * visualization.boxSize,
              width: visualization.boxSize,
              height: visualization.boxSize,
              path: getBoxImagePath(grid[i][j])
            });
          }
        }
        visualization.boxes.push(hero)
      };

      // initialization
      var grid = [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 3, 1],
        [1, 1, 1, 1, 1, 1, 1, 1]];
      var initialPosition = findInitialPosition(grid);
      var gridSize = grid.length;
      var visualization = {
        width: 400,
        height: 400
      };
      visualization.boxSize = visualization.width / gridSize,
      reset();

      // public scope
      $scope.visualization = visualization;

      // interface
      mazeApi.listenRun(run);
      mazeApi.listenReset(reset);

    },
    link: function(scope, element){
    }
  };
}])
.filter('pixelCoordinates', function () {
  return function(input, visualization) {
    return input * visualization.boxSize;
  };
});


// ------------------------------------------------------------------

// constants for box types
var BoxType = {
  FREE: 0,
  WALL: 1,
  START: 2,
  GOAL:  3
};

// constructor for box object
/*function Box(row, col, width, height, path) {
    this.row = row;
    this.col = col;
    this.width = width;
    this.height = height;
    this.path = path;

    this.getX = function {
        return
    }
}*/

/*
    Find position of the start box
*/
function findInitialPosition(grid) {
  for (var i = 0; i < grid.length; i++) {
    for (var j = 0; j < grid[i].length; j++) {
      if (grid[i][j] == BoxType.START) {
        return [i, j];
      }
    }
  }
};


// image paths
var getBoxImagePath = function(box) {
  switch (box) {
    case BoxType.WALL: return '/static/img/box.svg';
    case BoxType.GOAL: return '/static/img/goal.png';
    default: return null;
  }
};
