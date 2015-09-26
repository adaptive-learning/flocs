/*
 * Maze Service
 */
angular.module('flocs.maze')
.factory('mazeService', ['BoxType', 'gridService',
  function(BoxType, gridService) {

  // NOTE: We use observer pattern to notify views. Alternative would be to use
  //       $broadcast (but it would pollute $rootScope).
  var viewList = [];
  var settings = null;
  var state = null;

  /**
  * Notify views about the maze change.
  */
  function notifyViewsMazeChanged() {
    angular.forEach(viewList, function(view) {
      view.mazeChanged();
    });
  }

  /**
  * Notify views about the hero change.
  */
  function notifyViewsHeroChanged() {
    angular.forEach(viewList, function(view) {
      view.heroChanged();
    });
  }

  /**
  * Register new directive to be updated by this service.
  * @param view Api object of the directive.
  */
  function registerView(view) {
    console.log('mazeService:register');
    viewList.push(view);
  }

  /**
  * Set new maze settings.
  * @param {Object} newSettings
  */
  function set(newSettings) {
    console.log('mazeService:set');
    settings = newSettings;
    reset();
  }

  /**
  * Reset maze settings.
  */
  function reset() {
    console.log('mazeService:reset');
    state = angular.copy(settings);
    notifyViewsHeroChanged();
  }

  /**
   * Move the hero 1 step in the current direction
   */
  function moveForward() {
    var movement = gridService.directionVector(state.hero.direction);
    state.hero.position[0] += movement[0];
    state.hero.position[1] += movement[1];
    //$rootScope.$broadcast('maze:move');
    //console.log('moveForward');
    //console.log('position: ', state.heroPosition, state.heroDirection);
    notifyViewsHeroChanged();
  }

  /*
   * Turn the hero by 90 degrees
   * @param turnDirection: 1 = turn left, -1 = turn right
   */
  function turn(turnDirection) {
    // NOTE: JavaScript modulo is not positive for positive inputs so we add 4
    // before taking modulo to make sure it's positive
    state.hero.direction = (state.hero.direction + turnDirection + 4) % 4;
    //$rootScope.$broadcast('maze:turn');
    //console.log('turn');
    notifyViewsHeroChanged();
  }

  /**
   * Return true if the hero reached the goal.
   */
  function solved() {
    var solved = (gridService.boxAt(state.grid, state.hero.position)
                  == BoxType.GOAL);
    return solved;
  }

  /**
   * Return true if the hero died.
   */
  function died() {
    var died = (gridService.boxAt(state.grid, state.hero.position)
                == BoxType.WALL);
    return died;
  }

  /**
   * Return current state
   */
  function getState() {
    return state;
  }

  // public API
  return {
    registerView: registerView,
    set: set,
    reset: reset,
    moveForward: moveForward,
    turn: turn,
    solved: solved,
    died: died,
    getState: getState
  };
}]);

