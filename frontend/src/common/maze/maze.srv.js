/**
 * Maze Service
 * @ngInject
 */
angular.module('flocs.maze')
.factory('mazeService', function(BoxType, SolidBlocks, gridService) {

  // NOTE: We use observer pattern to notify views. Alternative would be to use
  //       $broadcast (but it would pollute $rootScope).
  var viewList = [];
  var changeListeners = [];
  var settings = null;
  var state = null;


  /**
  * Notify views about the maze change.
  */
  function notifyViewsMazeChanged() {
    angular.forEach(viewList, function(view) {
      view.mazeChanged();
    });
    changeNotification();
  }

  /**
  * Notify views about a move of the hero.
  */
  function notifyViewsHeroChanged() {
    angular.forEach(viewList, function(view) {
      view.heroChanged();
    });
    changeNotification();
  }

  /**
  * Register new directive to be updated by this service.
  * @param view Api object of the directive.
  */
  function registerView(view) {
    //console.log('mazeService:register');
    viewList.push(view);
  }

  /**
   * Register new listener for changes
   */
  function addChangeListener(listener) {
    changeListeners.push(listener);
  }

  /**
   * Notify all change listeners about a change
   */
  function changeNotification() {
    angular.forEach(changeListeners, function(listener) {
      listener();
    });
  }

  /**
  * Set new maze settings.
  * @param {Object} newSettings
  */
  function set(newSettings) {
    //console.log('mazeService:set');
    settings = newSettings;
    reset();
  }

  /**
  * Reset maze settings.
  */
  function reset() {
    //console.log('mazeService:reset');
    state = angular.copy(settings);
    notifyViewsMazeChanged();
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
    // remove token if the robot step on it
    if (isToken(state.hero.position, true)) {
        notifyViewsMazeChanged();
    }
  }

  /**
   * Check if there is token on given position.
   * If remove flag is true, it will remove the token.
   *
   * @param position of checking
   * @param remove if true, it will remove token
   * @returns {boolean} true if there is token
   */
  function isToken(position, remove) {
      if (state.tokens === undefined) {
        return false;
      }
      for (var k = 0; k < state.tokens.length; k++) {
          if ((position[0] == state.tokens[k][0]) && (position[1] == state.tokens[k][1])) {
              // if remove is true, remove the token
              if (remove) {
                  state.tokens.splice(k, 1);
              }
              return true;
          }
      }
      return false;
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

  /*
   * Check if there is a clear path
   * @param checkDirection: 1 = check left, -1 = check right
   */
  function checkPath(checkDirection) {
    // NOTE: JavaScript modulo is not positive for positive inputs so we add 4
    // before taking modulo to make sure it's positive
    // direction to look at
    var direction = gridService.directionVector(
            (state.hero.direction + checkDirection + 4) % 4);
    // computed direction of box to be checked
    var checkPosition = [
            state.hero.position[0] + direction[0],
            state.hero.position[1] + direction[1]
        ];
    // is box free?
    var box = gridService.boxAt(state.grid, checkPosition);
    if (box === undefined) {
      return false;
    }
    // not a block thats cannot be walked through
    return SolidBlocks.indexOf(box) === -1;
  }

  /*
   * Returns BoxType constant to given string representation of box type
   * @param type: string representation of BoxType
   * @return corresponding BoxType constant (number)
   */
  function getBoxType(type) {
    // gets the boxtype constant from it name
    return BoxType[type];
  }

  /*
   * Check if the robot is on the specified type of box
   * @param boxType: any available BoxType
   * @return {boolean} true if robot is on the given type of box
   */
  function checkBox(boxType) {
    // direction of hero
    var checkPosition = [
      state.hero.position[0],
      state.hero.position[1]
    ];
    // get type of the box
    var box = gridService.boxAt(state.grid, checkPosition);

    // check undefined
    if (box === undefined) {
      return false;
    }

    // return whether the box is of color 'color'
    return box === boxType;
  }


  /**
   * Return true if the hero reached the goal.
   */
  function solved() {
    var isSolved = (gridService.boxAt(state.grid, state.hero.position) ==
                    BoxType.GOAL) &&
                   (getTokensAll() - getTokensPicked() === 0);
    return isSolved;
  }

  /**
   * Return true if the hero died.
   */
  function died() {
    var boxType = gridService.boxAt(state.grid, state.hero.position);
    return ((boxType == BoxType.WALL) || (boxType == BoxType.PIT));
  }

  /**
   * Return current state
   */
  function getState() {
    return state;
  }

  function getTokensPicked() {
    if (state.tokens === undefined) {
      return null;
    }
    return (settings.tokens.length - state.tokens.length);
  }

  function getTokensAll() {
    if (state.tokens === undefined) {
      return null;
    }
    var tokensTotal = settings.tokens.length;
    if (tokensTotal === 0) {
      return null;
    }
    return tokensTotal;
  }


   // public API
  return {
    registerView: registerView,
    addChangeListener: addChangeListener,
    set: set,
    reset: reset,
    moveForward: moveForward,
    turn: turn,
    checkPath: checkPath,
    checkBox: checkBox,
    getBoxType: getBoxType,
    solved: solved,
    died: died,
    getState: getState,
    getTokensPicked: getTokensPicked,
    getTokensAll: getTokensAll
  };
});

