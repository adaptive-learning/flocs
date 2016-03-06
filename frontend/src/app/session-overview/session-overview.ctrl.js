/*
 * Session overview controller
 */
angular.module('flocs.session-overview')
.controller('session-overviewCtrl', function($scope, $state, practiceService) {

  function cont() {
    $state.go('practice-start');
  }

  practiceService.gettingSessionOverview();
  $scope.overview = practiceService.sessionOverview;  
  $scope.cont = cont;

});
