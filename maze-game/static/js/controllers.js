/* Controllers */

angular.module('maze-game.controllers', [])

.controller('appCtrl', ['$scope', 'mazeApiService',
  function($scope, mazeApi) {

    function runClick() {
      mazeApi.run();
    };

    function resetClick() {
      mazeApi.reset();
    };

    mazeApi.listenSuccess(function(){alert('Solved!')});
    //mazeApi.listenFailure(...);

    $scope.runClick = runClick;
    $scope.resetClick = resetClick;

}]);
