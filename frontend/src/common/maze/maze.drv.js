/*
 * Maze Directive
 */
angular.module('flocs.maze')
.directive('flocsMaze', ['mazeService', 'BoxType', function(mazeService, BoxType) {
  return {
    restrict: 'E',
    scope: {},
    templateUrl: 'maze/maze.tpl.html',
    /*controller: function($scope){
    },*/
    link: function(scope, element, attrs) {

      // image paths
      var getBoxImagePath = function(box, token) {
        // if there is token, return token path
        if (token) {
          return '/static/assets/img/token.png';
        }
        switch (box) {
          case BoxType.WALL: return '/static/assets/img/box.svg';
          case BoxType.GOAL: return '/static/assets/img/goal.png';
          case BoxType.RED: return '/static/assets/img/red.jpg';
          case BoxType.GREEN: return '/static/assets/img/green.jpg';
          case BoxType.BLUE: return '/static/assets/img/blue.jpg';
          default: return null;
        }
      };

      var getHeroImagePath = function(direction) {
        switch(direction) {
            case 0:
                return '/static/assets/img/robot_small_right.svg';
            case 1:
                return '/static/assets/img/robot_small_back.svg';
            case 2:
                return '/static/assets/img/robot_small_left.svg';
            case 3:
                return '/static/assets/img/robot_small_front.svg';
            default:
                // should not happen
                throw "Invalid direction " + direction;
                //return '/static/assets/img/robot_small_front.svg';
        }
        //return '/static/assets/img/karlik2.png';
      };

      function setMaze(state){
        // continue only if state is not null
        if (!state) {
          return;
        }

        var gridWidth = state.grid[0].length;
        var gridHeight = state.grid.length;

        scope.visualization = {};
        // TODO: unhardcode width
        scope.visualization.width = 400;
        scope.visualization.boxSize = scope.visualization.width / gridWidth;
        scope.visualization.height = gridHeight * scope.visualization.boxSize;

        scope.visualization.boxes = [];
        for (var i = 0; i < gridHeight; i++) {
          for (var j = 0; j < gridWidth; j++) {
            scope.visualization.boxes.push({
              x: j, // * visualization.boxSize,
              y: i, // * visualization.boxSize,
              width: scope.visualization.boxSize,
              height: scope.visualization.boxSize,
              path: getBoxImagePath(state.grid[i][j], mazeService.isToken([j,i], false))
            });
          }
        }
        scope.hero = {
          width: scope.visualization.boxSize,
          height: scope.visualization.boxSize
        };
        scope.visualization.boxes.push(scope.hero);
        setHero(state.hero);
      }

      function setHero(heroState) {
        // TODO: animations
        scope.hero.x = heroState.position[0];
        scope.hero.y = heroState.position[1];
        scope.hero.direction = heroState.direction;
        scope.hero.path = getHeroImagePath(heroState.direction);
        //scope..hero.x = 2; //heroState.position[0];
        //scope.visualization.boxes[scope.visualization.boxes.length - 1].x = 2;
      }

      function mazeChanged() {
        var settings = mazeService.getState();
        setMaze(settings);
      }

      function heroChanged() {
        var state = mazeService.getState();
        setHero(state.hero);
      }

      var viewApi = {
        mazeChanged: mazeChanged,
        heroChanged: heroChanged
      };

      // subscribe the view for notifications from mazeService
      mazeService.registerView(viewApi);
      mazeChanged();
    }
  };
}]);
