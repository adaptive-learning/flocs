angular.module('flocs.admin-stats')
.controller('adminStatsCtrl', function($scope, adminStatsService, $uibModal) {

  /* Set the width of the side navigation to 250px */
  function openNav() {
        document.getElementById("mySidenav").style.width = "250px";
  }

  /* Set the width of the side navigation to 0 */
  function closeNav() {
        document.getElementById("mySidenav").style.width = "20px";
  }

  function hideAll() {
    $scope.daily_stats = false;
    $scope.task_stats = false;
    $scope.concept_stats = false;
    $scope.block_stats = false;
    $scope.session_stats = false;
  }

  function showOne(stats) {
    $scope[stats] = true;
  }

  function switchTo(stats) {
    hideAll();
    showOne(stats);
    closeNav();
  }

  adminStatsService.gettingStatistics().then(function(statistics) {
      $scope.statistics = statistics;
    });
  closeNav(); // close navbar at the beginning
  $scope.daily_stats = true; // title statistics
  $scope.openNav = openNav;
  $scope.closeNav = closeNav;
  $scope.switchTo = switchTo;
});
