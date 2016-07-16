angular.module('flocs.statistics')
.controller('statisticsCtrl', function($scope, statisticsService) {

  statisticsService.gettingStatistics().then(function(statistics) {
      $scope.statistics = statistics;
  });
});
