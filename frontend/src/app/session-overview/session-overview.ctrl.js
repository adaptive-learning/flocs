/*
 * Session overview controller
 */
angular.module('flocs.session-overview')
.controller('session-overviewCtrl', function($scope, $state, practiceService) {

  function earnedCredits(taskInstances) {
    var sum = 0;
    taskInstances.forEach(function(inst) {
      sum += inst['earned-credits'];
    });
    return sum;
  }

  function appendPercentil(percentils, taskInstances) {
    for (var i=0; i<percentils.length; i++) {
      taskInstances[i].percentil = percentils[i];
    }
    return taskInstances;
  }



  practiceService.gettingSessionOverview().then(function() {
    var overview = practiceService.sessionOverview;      
    $scope.overview = overview;
    $scope.taskInstances = appendPercentil(overview.percentils, overview.taskInstances);
    $scope.earnedCredits = earnedCredits(overview.taskInstances);
  });

});
