/*
 * Profile controller
 */
angular.module('flocs.profile')
.controller('profileCtrl', function($scope, userService, practiceService) {
  userService.gettingUserDetails();
  practiceService.gettingPracticeInfo();
  $scope.user = userService.user;
  $scope.practiceInfo = practiceService.practiceInfo;
});
