angular.module('flocs.statistics')
.controller('statisticsCtrl', function($scope, userService, statisticsService) {

  function whenLogged() {
    $scope.logged = true;
    statisticsService.gettingStatistics().then(function(statistics) {
      $scope.statistics = statistics;
    });
  }

  function notLoggedNotification() {
    $scope.logged = false;
  }

  $scope.logged = null;
  userService.waitUntilLogged().then(whenLogged, null, notLoggedNotification);
});
