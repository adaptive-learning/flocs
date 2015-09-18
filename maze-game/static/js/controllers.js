/* Controllers */

angular.module('flocs.controllers', [])

.controller('appCtrl', ['$scope', function($scope) {
  // global configuration (user, language) functions go here
}])

.controller('practiceCtrl', ['$scope', 'taskFactory', 'interpreterFactory',
  'workspaceFactory', 'mazeFactory',
  function($scope, taskFactory, interpreterFactory, workspaceFactory, mazeFactory) {

    function nextTask() {
      var task = taskFactory.getNewTask();
      // TODO: workspaceFactory -> set toolbox
      mazeFactory.setNewTask(task);
    }

    function run() {
      var result = interpreterFactory.runCode();
      // TODO: report results to taskFactory
      if (result.solved) {
        // TODO: get new task from task factory
        // TODO: melo by se zobrazit az po vizualizaci :-)
        alert('Solved!');
      } else if (result.died) {
        alert('Died!');
      }
    }

    function reset() {
      // TODO: reset interpreter if it's still running
      mazeFactory.resetTask();
    }

    function runOrReset() {
      if ($scope.initialState) {
        $scope.initialState = false;
        run();
      } else if (!($scope.resetting)) {
        $scope.resetting = true;
        reset();
        $scope.initialState = true;
        $scope.resetting = false;
      }
    }

    // TODO: zobrazit vytvoreny kod, pokud byl beh uspesny (nad tlacitkem "Next
    // level")
    //mazeFactory.listenSuccess(function(){alert('Solved!')});
    //var code = workspaceFactory.getJavaScriptCode();
    //console.log(code);
    //mazeFactory.listenFailure(...);

    // inital state = program can be run
    $scope.initialState = true;
    $scope.resetting = false;

    // set first task
    nextTask();

    // public functions
    $scope.runOrReset = runOrReset;

}]);
