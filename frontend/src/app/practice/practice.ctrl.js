/*
 * Main practice controller
 */
angular.module('flocs.practice')
.controller('practiceCtrl', ['$scope', 'practiceSessionService',
    function($scope, practiceSessionService) {

  // just start a new practice session
  practiceSessionService.startPracticeSession();

}]);

